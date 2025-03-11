RUN = poetry run

test:
	$(RUN) python -m unittest tests/test_*py tests/*/test_*py

# not yet deployed
doctest:
	find src docs -type f \( -name "*.rst" -o -name "*.md" -o -name "*.py" \) -print0 | xargs -0 $(RUN) python -m doctest --option ELLIPSIS --option NORMALIZE_WHITESPACE

%-doctest: %
	$(RUN) python -m doctest --option ELLIPSIS --option NORMALIZE_WHITESPACE $<

## Compiled

MODELS = ontology_metadata  obograph  validation_datamodel summary_statistics_datamodel lexical_index mapping_rules_datamodel text_annotator oxo taxon_constraints similarity search_datamodel cross_ontology_diff association class_enrichment value_set_configuration fhir mapping_cluster_datamodel cx item_list input_specification

pyclasses: $(patsubst %, src/oaklib/datamodels/%.py, $(MODELS))
jsonschema: $(patsubst %, src/oaklib/datamodels/%.schema.json, $(MODELS))
owl: $(patsubst %, src/oaklib/datamodels/%.owl.ttl, $(MODELS))

src/oaklib/datamodels/%.py: src/oaklib/datamodels/%.yaml
#	$(RUN) gen-pydantic $< > $@.tmp && mv $@.tmp $@
	$(RUN) gen-python $< > $@.tmp && mv $@.tmp $@
	$(RUN) tox -e lint

src/oaklib/datamodels/synonymizer.py: src/oaklib/datamodels/synonymizer.yaml
	$(RUN) gen-pydantic $< > $@.tmp && mv $@.tmp $@


src/oaklib/datamodels/%.schema.json: src/oaklib/datamodels/%.yaml
	$(RUN) gen-json-schema $< > $@.tmp && mv $@.tmp $@
src/oaklib/datamodels/%.owl.ttl: src/oaklib/datamodels/%.yaml
	$(RUN) gen-owl --no-metaclasses --no-type-objects $< > $@.tmp && mv $@.tmp $@

RUN_GENDOC = $(RUN) gen-doc --dialect myst
gendoc: gendoc-om gendoc-og gendoc-ss gendoc-val gendoc-mr gendoc-li gendoc-ann gendoc-search gendoc-xodiff gendoc-sim gendoc-assoc gendoc-tc gendoc-itemlist gendoc-ce

gendoc-om: src/oaklib/datamodels/ontology_metadata.yaml
	$(RUN_GENDOC)  $< -d docs/datamodels/ontology-metadata/
gendoc-og: src/oaklib/datamodels/obograph.yaml
	$(RUN_GENDOC)  $< -d docs/datamodels/obograph
gendoc-val: src/oaklib/datamodels/validation_datamodel.yaml
	$(RUN_GENDOC)  $< -d docs/datamodels/validation
gendoc-ss: src/oaklib/datamodels/summary_statistics_datamodel.yaml
	$(RUN_GENDOC)  $< -d docs/datamodels/summary-statistics
gendoc-sim: src/oaklib/datamodels/similarity.yaml
	$(RUN_GENDOC)  $< -d docs/datamodels/similarity
gendoc-li: src/oaklib/datamodels/lexical_index.yaml
	$(RUN_GENDOC)  $< -d docs/datamodels/lexical-index
gendoc-mr: src/oaklib/datamodels/mapping_rules_datamodel.yaml
	$(RUN_GENDOC)  $< -d docs/datamodels/mapping-rules
gendoc-ann: src/oaklib/datamodels/text_annotator.yaml
	$(RUN_GENDOC)  $< -d docs/datamodels/text-annotator
gendoc-search: src/oaklib/datamodels/search_datamodel.yaml
	$(RUN_GENDOC)  $< -d docs/datamodels/search
gendoc-xodiff: src/oaklib/datamodels/cross_ontology_diff.yaml
	$(RUN_GENDOC)  $< -d docs/datamodels/cross-ontology-diff
gendoc-assoc: src/oaklib/datamodels/association.yaml
	$(RUN_GENDOC)  $< -d docs/datamodels/association
gendoc-tc: src/oaklib/datamodels/taxon_constraints.yaml
	$(RUN_GENDOC)  $< -d docs/datamodels/taxon-constraints
gendoc-itemlist: src/oaklib/datamodels/item_list.yaml
	$(RUN_GENDOC)  $< -d docs/datamodels/item-list
gendoc-ce: src/oaklib/datamodels/class_enrichment.yaml
	$(RUN_GENDOC)  $< -d docs/datamodels/class-enrichment
gendoc-vsc: src/oaklib/datamodels/value_set_configuration.yaml
	$(RUN_GENDOC)  $< -d docs/datamodels/value-set-configuration

nb:
	$(RUN) jupyter notebook

sphinx-%:
	cd docs && ( $(RUN) make $* )

# TODO: is there a better way?
# this relies on a separate folder with a checkout of the gh-pages branch
stage-docs:
	cp -pr docs/_build/html/* ../gh-pages/oaklib-gh-pages/

#gh-deploy

tests/input/%.owl: tests/input/%.obo
	robot convert -i $< -o $@

tests/input/%.ofn: tests/input/%.owl
	robot convert -i $< -o $@

tests/input/%.db: tests/input/%.owl
	$(RUN) semsql make $@

# create a convenient wrapper script;
# this can be used outside the poetry environment
bin/runoak:
	echo `poetry run which runoak` '"$$@"' > $@ && chmod +x $@

# Benchmarking for Semsimian
RUNOAK := $(shell which runoak)
SEMSIMIAN_HP_PROFILE = "oak_semsimian_hp.profile"
NON_SEMSIMIAN_HP_PROFILE = "oak_hp.profile"
SEMSIMIAN_PHENIO_PROFILE = "oak_semsimian_phenio.profile"
NON_SEMSIMIAN_PHENIO_PROFILE = "oak_phenio.profile"
HP_TERMS = "HPO_terms.txt"
MP_TERMS = "MP_terms.txt"
PROFILER_SCRIPT= "src/oaklib/implementations/semsimian/profiler.py"

run_benchmark: benchmarks profiles

benchmarks:
	time python -m cProfile -o $(SEMSIMIAN_HP_PROFILE) -s tottime $(RUNOAK) -i semsimian:sqlite:obo:hp similarity -p i,p HP:0002205 @ HP:0000166 HP:0012461 HP:0002167 HP:0012390 HP:0002840 HP:0002840 HP:0012432 > /dev/null
	time python -m cProfile -o $(NON_SEMSIMIAN_HP_PROFILE) -s tottime $(RUNOAK) -i sqlite:obo:hp similarity -p i,p HP:0002205 @ HP:0000166 HP:0012461 HP:0002167 HP:0012390 HP:0002840 HP:0002840 HP:0012432 > /dev/null

profiles:
	python $(PROFILER_SCRIPT) $(SEMSIMIAN_HP_PROFILE)
	python $(PROFILER_SCRIPT) $(NON_SEMSIMIAN_HP_PROFILE)

phenio-benchmarks:
	$(RUNOAK) -i sqlite:obo:hp descendants -p i HP:0000118 > $(HP_TERMS)
	$(RUNOAK) -i sqlite:obo:mp descendants -p i MP:0000001 > $(MP_TERMS)
	time python -m cProfile -o $(SEMSIMIAN_PHENIO_PROFILE) -s tottime $(RUNOAK) -i semsimian:sqlite:obo:phenio similarity -p i --set1-file $(HP_TERMS) --set2-file $(MP_TERMS) -O csv -o HP_vs_MP_semsimian.tsv
	time python -m cProfile -o $(NON_SEMSIMIAN_PHENIO_PROFILE) -s tottime $(RUNOAK) -i sqlite:obo:phenio similarity -p i --set1-file $(HP_TERMS) --set2-file $(MP_TERMS) -O csv -o HP_vs_MP_semsimian.tsv

phenio-profiles:
	python $(PROFILER_SCRIPT) $(SEMSIMIAN_PHENIO_PROFILE)
	python $(PROFILER_SCRIPT) $(NON_SEMSIMIAN_PHENIO_PROFILE)

