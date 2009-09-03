SPHINXOPTS      =
SPHINXBUILD     = sphinx-build
PAPER           =
DOCDIR          = doc
BUILT_DOCDIR    = $(DOCDIR)/built
PAPEROPT_a4     = -D latex_paper_size=a4
PAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS   = -d $(DOCDIR)/.doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .

GENERATED_FILES =							\
	sw/doc/messages.txt						\
	sw/onboard/generated/messages.h			\
	$(BUILT_DOCDIR)/onboard/xml/index.xml

################################################################################
# Main targets
################################################################################
onboard:
	@make -C sw/onboard/ all

bootloader:
	@make -C sw/bootloader/ all

doc: mkdir $(GENERATED_FILES) html

all: onboard bootloader doc

clean:
	-rm -rf $(BUILT_DOCDIR) $(DOCDIR)/.doctrees $(GENERATED_FILES)
	@make -C sw/groundstation/ clean
	@make -C sw/onboard/ clean
	@make -C sw/bootloader/ clean

test: clean
	@make -C sw/groundstation/ test
	@cd sw/onboard ; ./build-tests.sh

showdoc: doc
	@firefox doc/built/html/index.html

################################################################################
# Dependencies
################################################################################
mkdir:
	@mkdir -p $(BUILT_DOCDIR)

$(BUILT_DOCDIR)/onboard/xml/index.xml: sw/onboard/doxygen.cfg
	@DOCDIR=$(DOCDIR) BUILT_DOCDIR=$(BUILT_DOCDIR) doxygen $<

sw/doc/messages.txt: sw/onboard/config/messages.xml
	@PYTHONPATH=./sw/groundstation/ ./sw/tools/gen-messages.py -m $< -f rst > $@

sw/onboard/generated/messages.h: sw/onboard/config/messages.xml
	@make -C sw/onboard/ generated/messages.h

html:
	@$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) doc/built/html

.PHONY: doc clean test onboard bootloader
