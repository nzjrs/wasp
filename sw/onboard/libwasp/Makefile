Q                   = @
TOOLS               = ../../tools
MESSAGES            = ../config/messages.xml
SRCDIR              = ..
INCDIR              = ./include

LIB                 = ./lib/libwasp.a
OBJS                = comm.o messages.o

default: dir $(LIB)

dir:
	$(Q)test -d $(INCDIR) || mkdir -p $(INCDIR)

# Radio header
$(INCDIR)/build.h: $(SRC) $(TOOLS)/gen-build-info.py
	@echo GENERATE $@
	$(Q)PYTHONPATH=$(SRCDIR)/../groundstation/ $(TOOLS)/gen-build-info.py --target=$(TARGET) > $@

$(INCDIR)/messages.h: $(MESSAGES) $(TOOLS)/gen-messages.py
	@echo GENERATE $@
	$(Q)PYTHONPATH=$(SRCDIR)/../groundstation/ $(TOOLS)/gen-messages.py --messages=$< --format=header --output=$@

messages.c: $(MESSAGES) $(TOOLS)/gen-messages.py
	@echo GENERATE $@
	$(Q)PYTHONPATH=$(SRCDIR)/../groundstation/ $(TOOLS)/gen-messages.py --messages=$< --format=function --output=$@

generated: $(INCDIR)/build.h $(INCDIR)/messages.h messages.c

%.o: %.c
	@echo COMPILE $<
	$(Q)gcc -g -c -Wall -I$(INCDIR) $< -o $@

$(LIB):  headers-copy generated $(OBJS)
	@echo ARCHIVE $@
	$(Q)ar rcs $@ $(OBJS)

headers-copy: dir
	$(Q) cp $(SRCDIR)/std.h $(INCDIR)
	$(Q) cp $(SRCDIR)/messages_types.h $(INCDIR)

clean:
	$(Q) rm -f $(LIB)
	$(Q) rm -f $(OBJS)
	$(Q) rm -f $(INCDIR)/build.h
	$(Q) rm -f $(INCDIR)/messages.h
	$(Q) rm -f $(INCDIR)/std.h
	$(Q) rm -f $(INCDIR)/messages_types.h
	$(Q) rm -f messages.c
	$(Q) rm -f test

test: test.c $(LIB)
	@echo COMPILE test
	$(Q)gcc -g -Wall -I$(INCDIR) -o $@ $^
