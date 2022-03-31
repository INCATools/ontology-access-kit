RUN = poetry run

test:
	$(RUN) python -m unittest tests/test_*py tests/*/test_*py

## Compiled

MODELS = ontology_metadata  obograph  validation_datamodel summary_statistics_datamodel lexical_index mapping_rules_datamodel

#pyclasses: src/obolib/vocabulary/ontology_metadata.py  src/obolib/vocabulary/obograph.py  src/obolib/vocabulary/validation_datamodel.py src/obolib/vocabulary/summary_statistics_datamodel.py
pyclasses: $(patsubst %, src/obolib/vocabulary/%.py, $(MODELS))

src/obolib/vocabulary/%.py: src/obolib/vocabulary/%.yaml
	$(RUN) gen-python $< > $@.tmp && mv $@.tmp $@

gendoc: gendoc-om gendoc-og gendoc-ss gendoc-val gendoc-mr gendoc-li

gendoc-om: src/obolib/vocabulary/ontology_metadata.yaml
	$(RUN) gen-doc $< -d docs/datamodels/ontology-metadata/
gendoc-og: src/obolib/vocabulary/obograph.yaml
	$(RUN) gen-doc $< -d docs/datamodels/obograph
gendoc-val: src/obolib/vocabulary/validation_datamodel.yaml
	$(RUN) gen-doc $< -d docs/datamodels/validation
gendoc-ss: src/obolib/vocabulary/summary_statistics_datamodel.yaml
	$(RUN) gen-doc $< -d docs/datamodels/summary-statistics
gendoc-li: src/obolib/vocabulary/lexical_index.yaml
	$(RUN) gen-doc $< -d docs/datamodels/lexical-index
gendoc-mr: src/obolib/vocabulary/mapping_rules_datamodel.yaml
	$(RUN) gen-doc $< -d docs/datamodels/mapping-rules

nb:
	$(RUN) jupyter notebook

sphinx-%:
	cd docs && ( $(RUN) make $* )

# TODO: is there a better way?
# this relies on a separate folder with a checkout of the gh-pages branch
stage-docs:
	cp -pr docs/_build/html/* ../gh-pages/obolib-gh-pages/

#gh-deploy
