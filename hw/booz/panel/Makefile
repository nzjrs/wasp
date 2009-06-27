GERBMERGE = gerbmerge
GERBV = gerbv

CFG=layout.cfg
DEF=layout.def

panel:
	cd ..; make gerber; make -f Makefile.mirror gerber
	$(GERBMERGE) $(CFG) $(DEF)

view: panel
	$(GERBV) merged.*.ger

clean:
	rm -f merged.* *~
