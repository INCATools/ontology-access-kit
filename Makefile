RUN = poetry run

test:
	$(RUN) python -m unittest tests/test_*py

## Compiled

src/obolib/vocabulary/ontology_metadata.py: src/obolib/vocabulary/ontology_metadata.yaml
	$(RUN) gen-python $< > $@.tmp && mv $@.tmp $@

gendoc: src/obolib/vocabulary/ontology_metadata.yaml
	$(RUN) gen-doc $< -d docs/vocabulary

nb:
	$(RUN) jupyter notebook

sphinx-%:
	cd docs && ( $(RUN) make $* )
