from dataclasses import dataclass
from typing import Any

import yaml

from oaklib import BasicOntologyInterface
from oaklib.datamodels.vocabulary import (
    CONTRIBUTOR,
    CREATOR,
    DESCRIPTION,
    RDFS_COMMENT,
    RDFS_LABEL,
    RDFS_SEE_ALSO,
    SKOS_DEFINITION_CURIE,
    TITLE,
)
from oaklib.io.streaming_writer import StreamingWriter
from oaklib.utilities.ontology_metadata_utils import (
    map_license_to_url,
    map_license_url_to_name,
    normalize_url,
    person_by_orcid,
)

# hardcode the two main creators for now
DEFAULT_CREATOR = "orcid:0000-0002-6601-2165"
BIO2OBO_DEFAULT_CREATOR = "orcid:0000-0003-4423-4370"

ENHANCED_PERSON_METADATA = {
    DEFAULT_CREATOR: {
        "github": "cmungall",
        "email": "cjmungall@lbl.gov",
    },
    BIO2OBO_DEFAULT_CREATOR: {
        "github": "cthoyt",
        "email": "cthoyt@gmail.com",
    },
}


@dataclass
class OboFoundryMarkdownWriter(StreamingWriter):
    """
    A writer that emits ontology metadata as OBO Foundry markdown.

    Status: Experimental
    """

    def emit(self, obj: dict, label_fields=None):
        def _get(*keys: str, default=None, sv=True) -> Any:
            if keys:
                k = keys[0]
                if k in obj:
                    vs = obj[k]
                    vs = [normalize_url(v, ensure_https=False) for v in vs if isinstance(v, str)]
                    if sv:
                        v = vs[0] if vs else None
                    else:
                        v = vs
                    return v
                return _get(*keys[1:], default=default)
            return default

        adapter = BasicOntologyInterface()
        cc = adapter.converter
        id = _get("id")
        desc = _get(
            SKOS_DEFINITION_CURIE,
            DESCRIPTION,
            "dce:description",
            TITLE,
            RDFS_LABEL,
            RDFS_COMMENT,
            default="NO DESCRIPTION",
        )
        short_desc = desc
        if "." in desc:
            short_desc = desc.split(".")[0]
        prefix = _get("sh:prefix")
        created_by = _get(
            "schema:creator",
            CREATOR,
            "oio:auto-generated-by",
            CONTRIBUTOR,
            "dce:contributor",
            default=DEFAULT_CREATOR,
        )
        is_bio2obo = created_by.startswith("bio2obo:")
        aggregator = None
        if is_bio2obo:
            aggregator = "biopragmatics"
        # provided_by = _get("http://purl.org/pav/providedBy", default=created_by)
        id = normalize_url(id, ensure_https=False)
        full_id = id
        url = _get("schema:url", default=full_id)
        homepage = _get(RDFS_SEE_ALSO, default=url)
        if "github" in homepage:
            tracker = homepage + "/issues"
            repo = homepage
        else:
            repo = url
            tracker = url
        prefix_expansion = "/".join(url.split("/")[0:-1]) + "/"
        domain = "upper"
        if ":" not in prefix_expansion:
            if prefix_expansion == "obo":
                prefix_expansion = "http://purl.obolibrary.org/obo/"
            else:
                prefix_expansion = cc.expand(prefix_expansion + ":")
        if "/" in id:
            id = id.split("/")[-1]
        if ":" in id:
            id = id.split(":")[-1]
        if "." in id:
            id = id.split(".")[0]
        if "-" in id:
            id = id.replace("-", "_")
        title = _get(TITLE, "dce:title", RDFS_LABEL, default=id)
        if is_bio2obo:
            created_by = BIO2OBO_DEFAULT_CREATOR
            homepage = "https://biopragmatics.github.io/obo-db-ingest/"
            tracker = "https://github.com/biopragmatics/pyobo/issues"
            repo = "https://github.com/biopragmatics/obo-db-ingest"
            domain = "biological systems"
        person = person_by_orcid(created_by, ENHANCED_PERSON_METADATA)
        # TODO: query from metadata
        contact = person.model_dump()

        fmts = ["owl", "obo"]
        if is_bio2obo:
            fmts.append("sssom")

        def _product(fmt: str) -> dict:
            p = {
                "id": f"{id}.{fmt}",
                "title": f"{title} {fmt.upper()} release",
                "description": f"{fmt.upper()} release of {title}",
                "aggregator": aggregator,
            }
            if is_bio2obo:
                p["ontology_purl"] = f"https://w3id.org/biopragmatics/resources/{id}/{id}.{fmt}"
            return p

        products = [_product(fmt) for fmt in fmts]

        obo_metadata = {
            "layout": "ontology_detail",
            "activity_status": "active",
            "id": id,
            "title": title,
            "description": short_desc,
            "domain": domain,
            "preferredPrefix": prefix,
            "contact": contact,
            "homepage": homepage,
            "tracker": tracker,
            "repository": repo,
            "products": products,
        }
        if prefix_expansion:
            obo_metadata["uri_prefix"] = prefix_expansion
        license = _get("dcterms:license", "dcterms:rights", "dce:license")
        if license:
            license_url = map_license_to_url(license)
            license_name = map_license_url_to_name(license_url)
            license_name = license_name.replace("-", " ")
            obo_metadata["license"] = {"label": license_name, "url": license_url}
        obo_metadata_yaml = yaml.dump(obo_metadata, sort_keys=False)
        md = "---\n" + obo_metadata_yaml + "---\n\n" + desc + "\n"
        self.file.write(md)
