from typing import Dict, List, TextIO

from airium import Airium
from linkml_runtime.dumpers import json_dumper, yaml_dumper


def format_object(curie, label):
    if label:
        return f"{label} [{curie}]"
    else:
        return curie


def add_association_group(doc: Airium, associations: List[Dict], subject: str, header_label: str):
    associations_for_subject = [a for a in associations if a.get("subject") == subject]
    if associations_for_subject:
        with doc.div(klass="association-group"):
            doc.div(_t=header_label, klass="association-group-header")
            with doc.ul(klass="association-group-list"):
                for association in associations_for_subject:
                    label = format_object(
                        association.get("object"), association.get("object_label")
                    )
                    doc.li(_t=label)


def generate_html(subjects: List[str], groups: List[Dict]) -> str:
    doc = Airium()
    doc("<!DOCTYPE html>")
    with doc.html(lang="en"):
        with doc.head():
            doc.meta(charset="utf-8")
            doc.title(_t="Rollup Table")
            doc.style(
                _t="""
.rollup-table {
    border-collapse: collapse;
    width: 100%;
}
.rollup-table tr {
    vertical-align: top;
}
.rollup-table td {
    padding: 0.25rem;
    border-top: 1px solid black;
}
.primary-group-label {
    font-weight: bold;
}
.association-group {
    margin-bottom: 1rem;
}
.association-group-header {
    font-style: italic;
}
.association-group-list {
    margin: 0;
}
"""
            )

        with doc.body():
            with doc.table(klass="rollup-table"):
                with doc.tr():
                    doc.td(_t="Subject", klass="primary-group-label")
                    for subject in subjects:
                        doc.td(_t=subject)

                for group in groups:
                    with doc.tr():
                        label = format_object(
                            group.get("group_object"), group.get("group_object_label")
                        )
                        doc.td(_t=label, klass="primary-group-label")
                        for subject in subjects:
                            with doc.td():
                                for sub_group in group.get("sub_groups", []):
                                    add_association_group(
                                        doc,
                                        sub_group.get("associations", []),
                                        subject,
                                        format_object(
                                            sub_group.get("group_object"),
                                            sub_group.get("group_object_label"),
                                        ),
                                    )

                                add_association_group(
                                    doc, group.get("associations", []), subject, "Other"
                                )

    return str(doc)


def write_report(subjects: List[str], groups: List[Dict], output: TextIO, format: str):
    if format == "json":
        output.write(json_dumper.dumps(groups, inject_type=False))
    elif format == "yaml":
        output.write(yaml_dumper.dumps(groups))
    elif format == "html":
        output.write(generate_html(subjects, groups))
    else:
        raise ValueError(f"Unsupported format: {format}")
