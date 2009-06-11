SPHINXOPTS      =
SPHINXBUILD     = sphinx-build
PAPER           =
DOCDIR          = doc
BUILT_DOCDIR    = $(DOCDIR)/built
PAPEROPT_a4     = -D latex_paper_size=a4
PAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS   = -d $(DOCDIR)/.doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .

doc: mkdir generated html

generated: $(BUILT_DOCDIR)/onboard/xml/index.xml sw/doc/messages.rst

mkdir:
	@mkdir -p $(BUILT_DOCDIR)

$(BUILT_DOCDIR)/onboard/xml/index.xml:
	DOCDIR=$(DOCDIR) BUILT_DOCDIR=$(BUILT_DOCDIR) doxygen sw/onboard/doxygen.cfg

sw/doc/messages.rst: sw/onboard/conf-john/messages.xml
	./sw/tools/gen-messages.py -m sw/onboard/conf-john/messages.xml -f rst > sw/doc/messages.rst

html:
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) doc/built/html
	@echo
	@echo "Build finished. The HTML pages are in doc/html."

clean:
	-rm -rf $(BUILT_DOCDIR) $(DOCDIR)/.doctrees

.PHONY: doc clean
