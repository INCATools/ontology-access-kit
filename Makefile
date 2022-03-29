RUN = poetry run

test:
	$(RUN) python -m unittest tests/test_*py

## Compiled

pyclasses: src/obolib/vocabulary/ontology_metadata.py  src/obolib/vocabulary/obograph.py

src/obolib/vocabulary/%.py: src/obolib/vocabulary/%.yaml
	$(RUN) gen-python $< > $@.tmp && mv $@.tmp $@

gendoc: gendoc-om gendoc-og

gendoc-om: src/obolib/vocabulary/ontology_metadata.yaml
	$(RUN) gen-doc $< -d docs/datamodels/ontology-metadata/
gendoc-og: src/obolib/vocabulary/obograph.yaml
	$(RUN) gen-doc $< -d docs/datamodels/obograph

nb:
	$(RUN) jupyter notebook

sphinx-%:
	cd docs && ( $(RUN) make $* )

# TODO: is there a better way?
# this relies on a separate folder with a checkout of the gh-pages branch
stage-docs:
	cp -pr docs/_build/html/* ../gh-pages/obolib-gh-pages/

#gh-deploy
