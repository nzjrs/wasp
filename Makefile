SPHINXOPTS      =
SPHINXBUILD     = sphinx-build
PAPER           =
DOCDIR          = doc
BUILT_DOCDIR    = $(DOCDIR)/built
PAPEROPT_a4     = -D latex_paper_size=a4
PAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS   = -d $(DOCDIR)/.doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .

GENERATED_FILES =							\
	sw/doc/comm-protocol.rst				\
	sw/doc/settings.rst						\
	sw/onboard/generated/messages.h			\
	$(BUILT_DOCDIR)/onboard/xml/index.xml

################################################################################
# Main targets
################################################################################
onboard:
	@make -C sw/onboard/ all

bootloader:
	@make -C sw/bootloader/ all

BOOTLOADER_DEV=/dev/ttyUSB0
install_bootloader: bootloader
	lpc21isp -control sw/bootloader/bl.hex $(BOOTLOADER_DEV) 38400 12000

doc: mkdir html

all: onboard bootloader doc

clean: cleandoc
	@make -C sw/groundstation/ clean
	@make -C sw/onboard/ clean
	@make -C sw/bootloader/ clean

cleandoc:
	-rm -rf $(BUILT_DOCDIR) $(DOCDIR)/.doctrees $(GENERATED_FILES)

test: clean
	@make -C sw/groundstation/ test
	@cd sw/onboard ; ./build-tests.sh

showdoc: doc
	@gnome-www-browser doc/built/html/index.html

uploaddoc: doc
	-rsync -av doc/built/html/* root@greenbirdsystems.com:/var/www/waspuav.org/doc/

dist:
	@git archive --format=tar --prefix=wasp/ HEAD:sw | gzip > $(shell git rev-parse --verify HEAD)-$(shell git symbolic-ref HEAD | cut -d / -f 3)-sw.tar.gz
	@echo Created $(shell git rev-parse --verify HEAD)-$(shell git symbolic-ref HEAD | cut -d / -f 3)-sw.tar.gz
	@git archive --format=tar --prefix=wasp/ HEAD:hw | gzip > $(shell git rev-parse --verify HEAD)-$(shell git symbolic-ref HEAD | cut -d / -f 3)-hw.tar.gz
	@echo Created $(shell git rev-parse --verify HEAD)-$(shell git symbolic-ref HEAD | cut -d / -f 3)-hw.tar.gz
	@git archive --format=tar --prefix=wasp/ HEAD | gzip > $(shell git rev-parse --verify HEAD)-$(shell git symbolic-ref HEAD | cut -d / -f 3).tar.gz
	@echo Created $(shell git rev-parse --verify HEAD)-$(shell git symbolic-ref HEAD | cut -d / -f 3).tar.gz

release: dist uploaddoc
	@rsync -av $(shell git rev-parse --verify HEAD)-$(shell git symbolic-ref HEAD | cut -d / -f 3)*.tar.gz john@open.grcnz.com:/srv/default/http/downloads/wasp/

################################################################################
# Dependencies
################################################################################
mkdir:
	@mkdir -p $(BUILT_DOCDIR)

$(BUILT_DOCDIR)/onboard/xml/index.xml: sw/onboard/doxygen.cfg sw/onboard/*.h
	@DOCDIR=$(DOCDIR) BUILT_DOCDIR=$(BUILT_DOCDIR) doxygen $<
	#this is a hack, sphinx does not notice the changed xml
	@rm -f doc/built/html/sw/doc/onboard-api.html
	@rm -f doc/.doctrees/sw/doc/onboard-api.doctree

sw/doc/comm-protocol.rst: sw/onboard/config/messages.xml
	@PYTHONPATH=./sw/groundstation/ ./sw/tools/gen-messages.py -m $< -f rst --output=$@

sw/doc/settings.rst: sw/onboard/config/settings.xml
	@PYTHONPATH=./sw/groundstation/ ./sw/tools/gen-settings.py -s $< -f rst > $@

sw/onboard/generated/messages.h: sw/onboard/config/messages.xml
	@make -C sw/onboard/ generated/messages.h

html: $(GENERATED_FILES)
	@$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) doc/built/html

.PHONY: doc clean test onboard bootloader
