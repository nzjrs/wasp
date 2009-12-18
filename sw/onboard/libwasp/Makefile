Q                   = @
TOOLS               = ../../tools
MESSAGES            = ../config/messages.xml
LIBDIR              = .
SRCDIR              = ..

INCDIR              = $(LIBDIR)/include
PRIVINCDIR          = $(LIBDIR)/include/private

default: dir lib headers-copy

dir:
	$(Q)test -d $(LIBDIR) || mkdir -p $(LIBDIR)
	$(Q)test -d $(INCDIR) || mkdir -p $(INCDIR)
	$(Q)test -d $(PRIVINCDIR) || mkdir -p $(PRIVINCDIR)

# Radio header
$(PRIVINCDIR)/build.h: $(SRC) $(TOOLS)/gen-build-info.py
	@echo GENERATE $@
	$(Q)PYTHONPATH=$(SRCDIR)/../groundstation/ $(TOOLS)/gen-build-info.py --target=$(TARGET) > $@

$(PRIVINCDIR)/messages.h: $(MESSAGES) $(TOOLS)/gen-messages.py
	@echo GENERATE $@
	$(Q)PYTHONPATH=$(SRCDIR)/../groundstation/ $(TOOLS)/gen-messages.py --messages=$< > $@

$(PRIVINCDIR)/messages-lib.h: $(MESSAGES) $(TOOLS)/gen-messages.py
	@echo GENERATE $@
	$(Q)PYTHONPATH=$(SRCDIR)/../groundstation/ $(TOOLS)/gen-messages.py --messages=$< --format=inlinefunction > $@

generated: $(PRIVINCDIR)/build.h $(PRIVINCDIR)/messages.h $(PRIVINCDIR)/messages-lib.h

$(LIBDIR)/comm.o: comm.c
	@echo COMPILE comm.o
	$(Q)gcc -g -c -Wall -I$(PRIVINCDIR) $< -o $(@)

lib:  headers-copy generated $(LIBDIR)/comm.o
	$(Q)ar rcs libwasp.a $(LIBDIR)/comm.o

headers-copy: dir
	$(Q) cp $(SRCDIR)/std.h $(PRIVINCDIR)
	$(Q) cp $(SRCDIR)/messages_types.h $(PRIVINCDIR)

clean:
	$(Q) rm -f libwasp.a
	$(Q) rm -f $(LIBDIR)/comm.o
	$(Q) rm -f $(PRIVINCDIR)/std.h
	$(Q) rm -f $(PRIVINCDIR)/messages_types.h

