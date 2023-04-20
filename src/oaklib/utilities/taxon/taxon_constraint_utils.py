import logging
from typing import Iterator, TextIO

from oaklib.datamodels.taxon_constraints import SubjectTerm, Taxon, TaxonConstraint


def parse_gain_loss_file(file: TextIO) -> Iterator[SubjectTerm]:
    """
    Parses a file containing gains and losses

    See `<https://github.com/geneontology/go-ontology/issues/16298>`_

    :param file:
    :return:
    """
    for line in file.readlines():
        [term, event_text] = line.strip().split(",")
        st = SubjectTerm(term)
        parts = event_text.split(";")
        if parts[-1] == "":
            parts.pop()
        curr = None
        curr_category = None
        for part in parts:
            if not part:
                logging.error(f"Blank element in line {line}")
                continue
            if "|" in part:
                [category, taxon] = part.split("|")
                curr_category = category
                if category == "Gain":
                    curr = st.only_in
                elif category == ">Loss":
                    curr = st.never_in
                else:
                    raise ValueError(f"Unknown directive: {category}")
            else:
                taxon = part
            if curr is None:
                raise ValueError("Need to specify directive")
            import re

            match = re.search(r"(\S+)\((.*)\)", taxon)
            if match:
                taxon_id, taxon_label = match.group(1, 2)
            else:
                raise ValueError(f"Could not parse taxon {taxon}")
            curr.append(
                TaxonConstraint(taxon=Taxon(taxon_id, label=taxon_label), evolutionary=True)
            )
            if curr_category == "Gain":
                curr = st.present_in
        yield st
