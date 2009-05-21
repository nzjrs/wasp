# Makefile for Sphinx documentation
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
PAPER         =

# Internal variables.
PAPEROPT_a4     = -D latex_paper_size=a4
PAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS   = -d doc/.doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .

.PHONY: html

html:
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) doc/built/html
	@echo
	@echo "Build finished. The HTML pages are in doc/html."

clean:
	-rm -rf doc/built doc/.doctrees


