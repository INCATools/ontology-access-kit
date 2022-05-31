RUN = poetry run

test:
	$(RUN) python -m unittest tests/test_*py tests/*/test_*py

## Compiled

MODELS = ontology_metadata  obograph  validation_datamodel summary_statistics_datamodel lexical_index mapping_rules_datamodel text_annotator oxo taxon_constraints similarity search_datamodel cross_ontology_diff

pyclasses: $(patsubst %, src/oaklib/datamodels/%.py, $(MODELS))
jsonschema: $(patsubst %, src/oaklib/datamodels/%.schema.json, $(MODELS))

src/oaklib/datamodels/%.py: src/oaklib/datamodels/%.yaml
	$(RUN) gen-python $< > $@.tmp && mv $@.tmp $@
src/oaklib/datamodels/%.schema.json: src/oaklib/datamodels/%.yaml
	$(RUN) gen-json-schema $< > $@.tmp && mv $@.tmp $@

gendoc: gendoc-om gendoc-og gendoc-ss gendoc-val gendoc-mr gendoc-li gendoc-ann gendoc-search gendoc-xodiff

gendoc-om: src/oaklib/datamodels/ontology_metadata.yaml
	$(RUN) gen-doc $< -d docs/datamodels/ontology-metadata/
gendoc-og: src/oaklib/datamodels/obograph.yaml
	$(RUN) gen-doc $< -d docs/datamodels/obograph
gendoc-val: src/oaklib/datamodels/validation_datamodel.yaml
	$(RUN) gen-doc $< -d docs/datamodels/validation
gendoc-ss: src/oaklib/datamodels/summary_statistics_datamodel.yaml
	$(RUN) gen-doc $< -d docs/datamodels/summary-statistics
gendoc-li: src/oaklib/datamodels/lexical_index.yaml
	$(RUN) gen-doc $< -d docs/datamodels/lexical-index
gendoc-mr: src/oaklib/datamodels/mapping_rules_datamodel.yaml
	$(RUN) gen-doc $< -d docs/datamodels/mapping-rules
gendoc-ann: src/oaklib/datamodels/text_annotator.yaml
	$(RUN) gen-doc $< -d docs/datamodels/text-annotator
gendoc-search: src/oaklib/datamodels/search_datamodel.yaml
	$(RUN) gen-doc $< -d docs/datamodels/search
gendoc-xodiff: src/oaklib/datamodels/cross_ontology_diff.yaml
	$(RUN) gen-doc $< -d docs/datamodels/cross-ontology-diff

nb:
	$(RUN) jupyter notebook

sphinx-%:
	cd docs && ( $(RUN) make $* )

# TODO: is there a better way?
# this relies on a separate folder with a checkout of the gh-pages branch
stage-docs:
	cp -pr docs/_build/html/* ../gh-pages/oaklib-gh-pages/

#gh-deploy

tests/input/%.db: tests/input/%.owl
	$(RUN) semsql make $@

# create a convenient wrapper script;
# this can be used outside the poetry environment
bin/runoak:
	echo `poetry run which runoak` '"$$@"' > $@ && chmod +x $@
