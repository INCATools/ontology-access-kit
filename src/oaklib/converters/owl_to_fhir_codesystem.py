"""Convert OWL to FHIR CodeSystem JSON

Resources
- Obographs: https://incatools.github.io/ontology-access-kit/interfaces/obograph.html
- Bioontologies
  - https://github.com/biopragmatics/bioontologies
  - https://bioontologies.readthedocs.io/en/latest/usage.html
- FHIR
  - CodeSystem: https://build.fhir.org/codesystem.html
- OAK PR: https://github.com/INCATools/ontology-access-kit/pull/320
- Upload examples here: https://drive.google.com/drive/folders/1lwGQ63_fedfWlGlRemq8OeZhZsvIXN01
- OWL::RDF mappings (not sure if useful here) https://www.w3.org/TR/2012/REC-owl2-mapping-to-rdf-20121211/

TODO's
  * Move this into GitHub issue (and link here) so I can get input on some of these more difficult parts / parts I don't yet understand
  1. Write converter MVP
    - paths to things to use (relative to root of Graph `g`):
      - nodes
      - edges
      ...
      - id
      - meta
      - description
      - license?
      - roots?
      - title
      - version
      - version_iri
  2. Add converter to OAK CLI
  3. Test(s)
  4. Improve converter

TODO's expanded
  4. Improve converter
  Paths to things to use (relative to root of Graph `g`):
  4.1. Obographs stuff
  4.1.1. propertyChainAxioms: understand & utilize
    "propertyChainAxioms" : [ {
      "predicateId" : "http://purl.obolibrary.org/obo/RO_0002566",
      "chainPredicateIds" : [ "http://purl.obolibrary.org/obo/RO_0002327", "http://purl.obolibrary.org/obo/RO_0002411", "http://purl.obolibrary.org/obo/RO_0002233" ]
    }, ...
  4.1.2. domainRangeAxioms: understand & utilize
    "domainRangeAxioms" : [ {
      "predicateId" : "http://purl.obolibrary.org/obo/RO_0002176",
      "domainClassIds" : [ "http://purl.obolibrary.org/obo/BFO_0000004" ]
    }, ...
  4.1.3. logicalDefinitionAxioms: understand & utilize
    "logicalDefinitionAxioms" : [ {
      "definedClassId" : "http://purl.obolibrary.org/obo/MONDO_0011258",
      "genusIds" : [ "http://purl.obolibrary.org/obo/MONDO_0018878" ],
      "restrictions" : [ {
        "propertyId" : "http://purl.obolibrary.org/obo/RO_0004003",
        "fillerId" : "http://identifiers.org/hgnc/3519"
      } ]
    }, ...
  4.1.4. meta: understand & utilize
    "meta" : {
      "subsets" : [ ],
      "xrefs" : [ ],
      "version": ...,
      "basicPropertyValues" : [ {
        "pred" : "http://purl.obolibrary.org/obo/IAO_0000700",
        "val" : "http://purl.obolibrary.org/obo/MONDO_0000001"
      }, ...
  4.1.5. equivalentNodesSets: understand & utilize?
    "equivalentNodesSets" : [ ],  # empty for Mondo
  4.2. aehrc/fhir-owl stuff
  4.2.1. filter[]: Look at the file I converted using fhir-owl, near the top.
  4.3. Obograph Node stuff
  4.3.1. See what all I can include from:
    - alternative_ids[], created_by, creation_date, definition, definition_provenance, id, lbl (label), synonyms[],
    - xrefs[] (I see the CURIE, but nothing else... does it not parse other xref info? or is it in axioms?),
    - meta.version?
  4.4. Anything else from FHIR CodeSystem?
  5. construct multiple CodeSystem resources for each collection of terms that isn't part of the main ontology
  6. put keys in my preferred order? so that lists are at the bottom

todo's (minor/later)
  1. bioontologies -> OAK when issue fixed: https://github.com/INCATools/ontology-access-kit/issues/321
  2. Schema mappings (Obograph -> FHIR CodeSystem). SchemaAutomator? Other approach?
  3. CodeSystem type: Dict -> Dataclass. Chris (2022/10/18)
  https://github.com/INCATools/ontology-access-kit/pull/320/files#r998844157: Rather than writing to dicts you could
  have an actual python datamodel for the FHIR code system and serialize this. This has numerous advantages such as
  type safety, clarity, ease of refactoring. See the src/datamodels folder for examples.
"""
import json
import os
import pickle
import sys
from datetime import datetime
from typing import Dict, List, Union


PROJECT_DIR = os.path.join(os.path.dirname(__file__), '..', '..', '..')
CACHE_DIR = os.path.join(PROJECT_DIR, 'cache')
JSON_TYPE = Union[Dict, List]
# SYNONYM_PROPERTY_LOOKUP: https://raw.githubusercontent.com/geneontology/go-ontology/master/contrib/oboInOwl
# todo: Shouldn't Obographs include oboInOwl URIs and not just assume users know about it? I shouldn't have to add here.
#  Should ask `bioontologies` devs if this is a `bioontologies` issue, and if not, make a GH issue in Obographs repo.
SYNONYM_PROPERTY_LOOKUP = {
    'hasExactSynonym': {
        'uri': 'http://www.geneontology.org/formats/oboInOwl#hasExactSynonym',
        'description':
            'An alias in which the alias exhibits true synonymy. Example: ornithine cycle is an exact synonym of urea '
            'cycle'
    },
    'hasNarrowSynonym': {
        'uri': 'http://www.geneontology.org/formats/oboInOwl#hasNarrowSynonym',
        'description':
            'An alias in which the alias is narrower than the primary class name. Example: pyrimidine-dimer repair by '
            'photolyase is a narrow synonym of photoreactive repair'
    },
    'hasBroadSynonym': {
        'uri': 'http://www.geneontology.org/formats/oboInOwl#hasBroadSynonym',
        'description':
            'An alias in which the alias is broader than the primary class name. Example: cell division is a broad '
            'synonym of cytokinesis'
    },
    'hasRelatedSynonym': {
        'uri': 'http://www.geneontology.org/formats/oboInOwl#hasRelatedSynonym',
        'description':
            'An alias in which the alias is related the primary class name, but not necessarily broader or narrower. '
            'Example: cytochrome bc1 complex is a related synonym of ubiquinol-cytochrome-c reductase activity; '
            'virulence is a related synonym of pathogenesis'
    },
    'hasSynonym': {
        'uri': 'http://www.geneontology.org/formats/oboInOwl#hasSynonym',
        'description': 'A relation between a class and an alias term.'
    },
}


# todo: This is for development purposes. can delete after or modify if needed
def _load_obograph(inpath: str, cache_dir=CACHE_DIR, save_cache=False, load_cache=True, verbose=True):
    """Load the obograph, storing from cache if necessary
    todo: would be nice if faster to load
     pickle https://stackoverflow.com/questions/66348333/speed-up-reading-multiple-pickle-files"""
    loaded_from_cache = False
    cache_filename = os.path.basename(inpath).replace('.owl', '.pickle')
    cache_path = os.path.join(cache_dir, cache_filename)
    if load_cache:
        if os.path.exists(cache_path):
            t1 = datetime.now()
            with open(cache_path, 'rb') as handle:
                parse_results = pickle.load(handle)
            t2 = datetime.now()
            loaded_from_cache = True
            if verbose:
                print(f'Loaded cache in {(t2 - t1).seconds} seconds')
        else:
            print('Attempted to load from cache, but cached file did not exist. Running conversion.')

    if not load_cache or (load_cache and not os.path.exists(cache_path)):
        # todo: When OAK issues fixed, use OAK
        #  i. performance https://github.com/INCATools/ontology-access-kit/issues/338
        #  ii. missing/incomplete properties https://github.com/INCATools/ontology-access-kit/issues/339
        # todo: When bioontologies performance issue (https://github.com/biopragmatics/bioontologies/issues/7) fixed,
        #  can move `from bioontologies import robot` up to the top
        t1 = datetime.now()
        from bioontologies import robot
        parse_results: robot.ParseResults = robot.convert_to_obograph_local(inpath)
        t2 = datetime.now()
        if verbose:
            print(f'Loaded obograph using robot through bioontologies in {(t2-t1).seconds} seconds')

    if save_cache and not loaded_from_cache:
        if not os.path.exists(CACHE_DIR):
            os.mkdir(CACHE_DIR)
        with open(cache_path, 'wb') as handle:
            # It can't be unbound given above logic, but PyCharm isn't smart enough to know that.
            # noinspection PyUnboundLocalVariable
            pickle.dump(parse_results, handle, protocol=pickle.HIGHEST_PROTOCOL)

    graph = parse_results.graph_document.graphs[0]
    return graph


def convert(
        inpath: str, outpath: str,
        # todo: code_system_uri_prefix: any way to know w/out user input except by (a) inference, e.g. most n nodes
        #  w/ the URI prefix, e.g. http://purl.obolibrary.org/obo/MONDO_ in http://purl.obolibrary.org/obo/MONDO_0000001
        #  or (ii) Obograph top level 'roots' property? (assuming they all share same URI prefix).
        #  (ii) will work if 'roots' are required by OWL. Here's how they appear in mondo.owl (IAO_0000700),
        #   ...and note that also non-Mondo class URI stems /may/ be ascertainable by terms:source.
        #     <owl:Ontology rdf:about="http://purl.obolibrary.org/obo/mondo.owl">
        #         <owl:versionIRI rdf:resource="http://purl.obolibrary.org/obo/mondo/releases/2022-07-01/mondo.owl"/>
        #         <obo:IAO_0000700 rdf:resource="http://purl.obolibrary.org/obo/MONDO_0000001"/>
        #         <terms:source rdf:resource="http://purl.obolibrary.org/obo/chebi.owl"/>
        code_system_uri_prefix: str,
        save_cache=False, load_cache=True,
        # TODO: These args should be added to CLI, but declared from global config dict w/ defaults
        add_exact_synonyms_to_properties=True,
        # todo: native_prefix_map: is there any use? maybe code_system_uri is sufficient
        # native_prefix_map: Dict[str, str] = None
) -> JSON_TYPE:
    """Convert

    :param add_exact_synonyms_to_properties (bool): oboInOwl has hasExactSynonym, hasNarrowSynonym, hasBroadSynonym, and
    hasRelatedSynonym. hasExactSynonym will always mapped to CodeSystem.concept.designation.use. Other synonyms will
    always be mapped to CodeSystem.concept.property. If add_exact_synonyms_to_properties==True, includes hasExactSynonym
    in CodeSystem.concept.property. This is a little redundant, but also useful if trying to view/query all synonyms in
    a single place.

    Side effects:
    - Writes file at `outpath`

    todo's (minor)
      1. Extending CodeSystem.concept.definition
        Examples:
          OWL:
            <owl:Axiom>
                <owl:annotatedSource rdf:resource="http://purl.obolibrary.org/obo/MONDO_0012333"/>
                <owl:annotatedProperty rdf:resource="http://purl.obolibrary.org/obo/IAO_0000115"/>
                <owl:annotatedTarget rdf:datatype="http://www.w3.org/2001/XMLSchema#string">Any autosomal recessive
                  nonsyndromic deafness in which the cause of the disease is a mutation in the COL11A2 gene.
                </owl:annotatedTarget>
                <oboInOwl:hasDbXref rdf:datatype="http://www.w3.org/2001/XMLSchema#string">MONDO:patterns/disease_series_by_gene</oboInOwl:hasDbXref>
            </owl:Axiom>
          Obographs (below is conversion from above OWL):
            "meta" : {
             "definition" : {
               "val" : "Any autosomal recessive nonsyndromic deafness in which the cause of the disease is a mutation in the COL11A2 gene.",
               "xrefs" : [ "MONDO:patterns/disease_series_by_gene" ]},
    """
    g = _load_obograph(inpath=inpath, save_cache=save_cache, load_cache=load_cache)

    cs = {
        # Static properties
        # - don't need any customization
        "resourceType": "CodeSystem",
        "hierarchyMeaning": "is-a",
        # TODO: Do I need to add something for any/all 'property' edges? aehrc/fhir-owl didn't have 'is_a'/parent
        # todo: root, deprecated: Add these back when I've actually used them. I think that I can pick out roots from
        #  obograph.root or something, and deprecated... i think there are different predicates that can be used, so
        #  i'll want to use those predicates themselves, and maybe map all the ones I'm aware of to a simple, common,
        #  explicit 'deprecated' property.
        "filter": [
        # {
        #     "code": "root",
        #     "operator": ["="],
        #     "value": "True or false."
        # }, {
        #     "code": "deprecated",
        #     "operator": ["="],
        #     "value": "True or false."
        # }
        ],
        "property": [{
            "code": "parent",
            "description": "Parent code, e.g. from relationship (<child> <is_a> <parent>)",
            "type": "code"
        },
        # {
        #     "code": "root",
        #     "description": "Indicates if this concept is a root concept (i.e. Thing is equivalent or a direct parent)",
        #     "type": "boolean"
        # }, {
        #     "code": "deprecated",
        #     "description": "Indicates if this concept is deprecated.",
        #     "type": "boolean"
        # }
        ],
        # Dynamic properties
        # TODO compute these
        "url": "http://purl.obolibrary.org/obo/mondo.owl",
        "version": "http://purl.obolibrary.org/obo/mondo/releases/2022-07-01/mondo.owl",
        "name": "http://purl.obolibrary.org/obo/mondo.owl",
        "valueSet": "http://purl.obolibrary.org/obo/mondo.owl?vs",

        # TODO: (i) Add to CLI, (ii) but use defaults
        #  - Define these in a dict at top. Then iter over to add argeparse args w/ defaults, & set here
        "status": "draft",
        "experimental": False,
        "description": "Includes Ontology(OntologyID(Anonymous-51)) [Axioms: 79310 Logical Axioms: 0]",
        "compositional": False,
        "versionNeeded": False,
        "content": "complete",
    }

    # Intermediaries
    # - cs_property_elements: Used to increase performance when checking for and adding new CodeSystem.property elements
    cs_property_element_set = set([x['code'] for x in cs['property']])

    foreign_nodes = {}  # todo: what to do with these?
    non_class_nodes = {}  # todo: what to do with these?
    unexpected_xref_patterns = set()
    concepts_d: JSON_TYPE = {}
    for node in g.nodes:
        code_or_id = node.id.replace(code_system_uri_prefix, '')
        exc_nonclass = node.type != 'CLASS'
        exc_foreign = code_or_id == node.id
        # todo: native prefixes (e.g. code_system_uri_prefix)
        #  i. I think that only top level classes 'native' by the ontology are supposed to be included. Because
        #   concept.code is not a URI or even a CURIE. So it is implicit that it is part of the CodeSystem defined by
        #   the URI. Thinking about this, it seems to me that a CodeSystem is a subset of an ontology that includes only
        #   native terms. So I should implement as such.
        #  ii. What to do if not an 'native' term? Add top level extension for these?
        if exc_nonclass or exc_foreign:
            lookup_d = non_class_nodes if exc_nonclass and not exc_foreign else foreign_nodes
            lookup_d[code_or_id] = {'node': node, 'property': []}
            continue

        # Top-level concept attributes
        concept_d = {"code": code_or_id, "property": []}
        if node.lbl:
            concept_d['display'] = node.lbl
        try:
            concept_d['definition'] = node.meta.definition.val
        except AttributeError:
            pass
        # TODO: What other things should I add, e.g. as extensions, e.g. URI

        # Synonyms
        synonyms = []
        try:
            synonyms = node.meta.synonyms if node.meta.synonyms else []
            concept_d['designation'] = []
        except AttributeError:
            pass
        # todo: add other property types other than synonyms (if they exist, which they probably do)
        #  - where located in graph? are they in edges?
        for syn in synonyms:
            for xref in syn.xrefs:
                # Synonyms 1: Determine properties
                # TODO: xref: Can this have URI and not CURIE? Check bionotologies.Synonym data model and/or add parsing
                #  for it (using curies.converter; but needs prefix map...)
                #  - syn_system: this is prob always CURIE. but where are CURIEs defined in OWL and Obographs?
                #   *sigh* what if not defined? I'm looking at mondo.owl and I see DOID:# in xrefs, but DOID not
                #   defined at top of file. This may be something to bring up as issue / ask Mondo ppl. but I should
                #   also account for. I think I should expect URIs.
                #  - syn_code: because of above, prolly no way to reliably get code from URI without complex
                #   inferential programming, e.g. looking for _ in URI and splitting on that. but prone to error.
                if xref.startswith('http'):
                    # TODO: Fix exception. this is not a proper xref
                    #  syn.xrefs = ['https://orcid.org/0000-0002-6601-2165']  # Chris Mungall
                    #  might want to bring this up to Chris et al. this seems like an error in Mondo
                    #      <owl:Axiom>
                    #         <owl:annotatedSource rdf:resource="http://purl.obolibrary.org/obo/MONDO_0000012"/>
                    #         <owl:annotatedProperty rdf:resource="http://www.geneontology.org/formats/oboInOwl#hasExactSynonym"/>
                    #         <owl:annotatedTarget rdf:datatype="http://www.w3.org/2001/XMLSchema#string">obsolete choreoathetosis (disease)</owl:annotatedTarget>
                    #         <oboInOwl:hasDbXref rdf:datatype="http://www.w3.org/2001/XMLSchema#string">https://orcid.org/0000-0002-6601-2165</oboInOwl:hasDbXref>
                    #     </owl:Axiom>
                    #  ... i think they were trying to obsolete it and it is the 'lazy' way to do so. just remove the original xref and put the orcid ID of the one who obsoleted
                    syn_code, syn_system = xref.split('_')[-1], xref.split('_')[:-1]
                    if '_' not in xref:  # TODO: examine above and verify correct
                        # TODO: Maybe best thing to do if no _ is to take whatever's after the last /
                        syn_code, syn_system = xref, xref
                        unexpected_xref_patterns.add(xref)
                else:
                    syn_code, syn_system = xref.split(':')[1], xref.split(':')[0]
                syn_type, syn_label = syn.pred, syn.val

                # Synonyms 2: Add data
                # Synonyms 2.1: CodeSystem.concept.designation.use
                if syn_type == 'hasExactSynonym':
                    concept_d['designation'].append({
                        "use": {
                            "system": syn_system,
                            "code": syn_code,
                            # todo: display: I got this from here, but is it correct?
                            # https://github.com/HOT-Ecosystem/hapi-fhir-jpaserver-starter/issues/64#issuecomment-1294284873
                            "display": "Synonym (core metadata concept)"},
                        "value": syn_label})
                if syn_type != 'hasExactSynonym' or (
                        syn_type == 'hasExactSynonym' and add_exact_synonyms_to_properties):
                    # Synonyms 2.2: CodeSystem.concept.property
                    # Uses (a) https://build.fhir.org/datatypes.html#Coding , but I also considered (b) CodeableConcept,
                    #  and(c), extension element.
                    concept_d['property'].append({
                        "code": syn_type,
                        "valueCoding": {
                            "system": syn_system,
                            "code": syn_code,
                            "display": syn_label}})
                    # Synonyms 2.3: CodeSystem.property
                    # todo: PyTypeChecker: Not sure why PyCharm is confused here
                    if syn_type not in cs_property_element_set:
                        cs_property_element_set.add(syn_type)
                        # todo: is there a semantic web way to specify 'null' or 'not found' instead of ''?
                        syn_info: Dict = SYNONYM_PROPERTY_LOOKUP.get(syn_type, {'uri': '', 'description': ''})
                        # noinspection PyTypeChecker
                        cs['property'].append({
                            "code": syn_type,
                            "uri": syn_info['uri'],
                            "description": syn_info['description'],
                            "type": "Coding"})  # type: # https://build.fhir.org/valueset-concept-property-type.html
        # TODO: Non-synonym properties
        #  - are these in nodes[] or edges[]? If nodes, add here.
        #  1. Non-synonym properties defined by aehrc/fhir-owl: and I want to include. But unlike them, I want
        #   to only include these properties on concepts themselves only if they are 'true'. The exception is 'parent',
        #   which I should always keep if the concept does have a parent. The properties are: parent, imported, root,
        #   & deprecated.
        #   1.1. add to CodeSystem.concept.property
        #   1.2. add to CodeSystem.property
        #  2. Non-synonym properties not inaehrc/fhir-owl
        concepts_d[code_or_id] = concept_d

    if foreign_nodes:  # todo: pre-set() and sort these?
        foreign_nodes_str = '\n'.join(set([x['node'].id for x in list(foreign_nodes.values())]))
        print(f'Excluding non-native nodes: {foreign_nodes_str}')
    if non_class_nodes:
        non_class_nodes_str = '\n'.join(set([x['node'].id for x in list(non_class_nodes.values())]))
        print(f'Excluding non-class nodes: {non_class_nodes_str}')
    if unexpected_xref_patterns:
        unexpected_xref_patterns_str = '\n'.join(unexpected_xref_patterns)
        print(f'Unanticipated URI patterns detected. '  # TODO: examine below
              f'Opting to set both system and code to these URIs rather than excluding: {unexpected_xref_patterns_str}',
              file=sys.stderr)

    # TODO: Edges
    # *_edges dicts: key(pred) -> vals(edges[])
    native_nodes_w_foreign_parent_edges = {}
    foreign_subject_edges = {}
    edge_subjs_with_no_nodes = {}
    edge_property_map = {'is_a': 'parent'}
    global_props  = set([x['code'] for x in cs['property']])
    # todo: added sub->obj to concept properties, but is obj->sub desirable/valid?
    # TODO: bugfix: Parents showing up multiple times:
    #         {
    #           "code": "parent",
    #           "valueCode": "0002974"
    #         },
    #         {
    #           "code": "parent",
    #           "valueCode": "0002974"
    #         }
    #       ],
    for edge in g.edges:
        # - Aggregate edge cases
        sub_code, obj_code = '', ''
        if edge.sub.startswith(code_system_uri_prefix):
            sub_code = edge.sub.replace(code_system_uri_prefix, '')
        if edge.obj.startswith(code_system_uri_prefix):
            obj_code = edge.sub.replace(code_system_uri_prefix, '')
        if not sub_code:
            if not edge.pred in foreign_subject_edges:
                foreign_subject_edges[edge.pred] = []
            foreign_subject_edges[edge.pred].append(edge)
        elif sub_code and not obj_code:
            if not edge.pred in native_nodes_w_foreign_parent_edges:
                native_nodes_w_foreign_parent_edges[edge.pred] = []
            native_nodes_w_foreign_parent_edges[edge.pred].append(edge)

        # Add to cs.property and concept.property
        prop_name: str = edge_property_map.get(edge.pred, edge.pred)
        sub_native = sub_code != ''
        code_or_id = sub_code if sub_code else edge.sub
        if prop_name not in global_props:
            # PyTypeChecker: No idea why PyCharm confused
            # noinspection PyTypeChecker
            cs['property'].append({
                "code": prop_name,
                "description": "",  # todo: how to get?
                "type": "code"})  # todo: code and not coding?
            global_props.add(prop_name)
        lookup_d = concepts_d if sub_native and code_or_id in concepts_d \
            else non_class_nodes if sub_native else foreign_nodes
        try:
            # TODO: There's various bugs here:
            #  i. multiple parents with same ID
            #  ii. edges being called parents
            #  iii. designation (system is wrong):
            #     {
            #       "use": {
            #         "system": "MONDORULE",
            #         "code": "1",
            #         "display": "Synonym (core metadata concept)"
            #       },
            #       "value": "mitochondrial DNA depletion syndrome type 2"
            #     },
            lookup_d[code_or_id]['property'].append({
                "code": "parent",
                "valueCode": obj_code if obj_code else edge.obj})
        except KeyError:
            if code_or_id not in edge_subjs_with_no_nodes:
                edge_subjs_with_no_nodes[code_or_id] = {'edges': []}
            edge_subjs_with_no_nodes[code_or_id]['edges'].append(edge)

    if edge_subjs_with_no_nodes:
        edge_subjs_with_no_nodes_str = '\n'.join(list(edge_subjs_with_no_nodes.keys()))
        print(f'Excluding edges with subjects that have no node: {edge_subjs_with_no_nodes_str}')

    # Add concepts to code system
    cs['count'] = len(concepts_d)
    cs['concept'] = list(concepts_d.values())

    pretty = False  # todo: cli param
    with open(outpath, 'w') as f:
        json.dump(cs, f, indent=2 if pretty else None)
    return cs


if __name__ == '__main__':  # todo: remove this when PR ready (this is for debugging; for some reason running test adds about ~7+ seconds)
    TEST_DIR = os.path.join(PROJECT_DIR, 'tests')
    convert(
        inpath=os.path.join(TEST_DIR, 'input', 'mondo-example.owl'),
        outpath=os.path.join(TEST_DIR, 'output', 'mondo-example.json'),
        code_system_uri_prefix='http://purl.obolibrary.org/obo/MONDO_',
        load_cache=True)
