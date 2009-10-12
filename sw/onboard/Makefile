TARGET          ?= autopilot_main
ARCH            ?= arm7
OBJDIR          = bin/$(ARCH)
Q               = @
TOOLS           = ../tools

include arch/Makefile.$(ARCH)

SRC =                               \
    $(TARGET).c                     \
    math/booz_trig_int.c            \
    math/pprz_geodetic_int.c        \
    math/pprz_geodetic_float.c      \
    rc.c                            \
    booz2_autopilot.c               \
    booz_ahrs_aligner.c             \
    booz2_filter_attitude_cmpl_euler.c \
    booz2_stabilization.c           \
    booz2_stabilization_rate.c      \
    booz2_stabilization_attitude.c  \
    booz2_guidance_h.c              \
    booz2_guidance_v.c              \
    booz2_ins.c                     \
    booz2_hf_float.c                \
    booz2_vf_float.c                \
    booz2_navigation.c              \
    booz2_fms.c                     \
    booz2_fms_datalink.c            \
    booz2_fms_test_signal.c         \
    comm.c                          \
    comm-autopilot.c                \
    settings.c

# Include arch specific sources
SRC += $(ARCHSRC)
ASMSRC = $(ARCHASMSRC)

# Define programs and commands.
REMOVE      = rm -f

# Compiler flags.
CFLAGS = -I. -I math -I arch
CFLAGS += -Os
CFLAGS += -Winline
CFLAGS += -Wall -Wcast-qual -Wimplicit -Wcast-align
CFLAGS += -Wpointer-arith -Wswitch
CFLAGS += -Wredundant-decls -Wreturn-type -Wshadow -Wunused
CFLAGS += -Wa,-adhlns=$(OBJDIR)/$(notdir $(subst $(suffix $<),.lst,$<))
CFLAGS += -Wstrict-prototypes -Wmissing-declarations
CFLAGS += -Wmissing-prototypes -Wnested-externs 
CFLAGS += -std=gnu99
CFLAGS += -fshort-enums
CFLAGS += -ffunction-sections
CFLAGS += -DARCH=$(ARCH)

INCLUDE_BUILD_INFO ?= 1
CFLAGS += -DINCLUDE_BUILD_INFO=$(INCLUDE_BUILD_INFO)

# Linker flags.
LDFLAGS = -n -nostartfiles -Wl,-Map=$(OBJDIR)/$(TARGET).map,--cref,-gc-sections
LDFLAGS += -lc
LDFLAGS += -lm

# Include arch specific flags
CFLAGS  += $(ARCHCFLAGS)
LDFLAGS += $(ARCHLDFLAGS)
ASFLAGS = $(ARCHASFLAGS)

# Define all object files.
COBJARM   = $(SRC:%.c=$(OBJDIR)/%.o)
AOBJARM   = $(ASMSRC:%.S=$(OBJDIR)/%.o)

# Define all list files
LST       = $(SRC:%.c=$(OBJDIR)/%.lst)
LST       += $(ASMSRC:%.S=$(OBJDIR)/%.lst)

# Default target.
all: build size

build: generated elf hex lss sym

elf: $(OBJDIR)/$(TARGET).elf
hex: $(OBJDIR)/$(TARGET).hex
lss: $(OBJDIR)/$(TARGET).lss 
sym: $(OBJDIR)/$(TARGET).sym

# Display MD5 of binary
md5: $(OBJDIR)/$(TARGET).elf
	@echo MD5 $(OBJDIR)/$(TARGET).elf
	$(Q)md5sum $(OBJDIR)/$(TARGET).elf

# Display size of file.
ELFSIZE = $(SIZE) -A $(OBJDIR)/$(TARGET).elf
size:
	@if [ -f $(OBJDIR)/$(TARGET).elf ]; then echo; $(ELFSIZE); echo; fi

# Program the device.  
LPC21IAP    = ../lpc21iap/lpc21iap
programmer:
	$(Q)cd `dirname $(LPC21IAP)` && make --quiet --no-print-directory Q=$(Q)
upload: $(OBJDIR)/$(TARGET).elf programmer
	@echo UPLOAD $(OBJDIR)/$(TARGET).elf
	$(Q)$(LPC21IAP)  $(OBJDIR)/$(TARGET).elf

# All generated headers
generated: generated/radio.h generated/build.h generated/messages.h generated/settings.h

# Radio header
generated/radio.h: config/radio.xml $(TOOLS)/gen-radio.py
	@echo GENERATE $@
	$(Q)PYTHONPATH=../groundstation/ $(TOOLS)/gen-radio.py $< > $@

generated/messages.h: config/messages.xml $(TOOLS)/gen-messages.py
	@echo GENERATE $@
	$(Q)PYTHONPATH=../groundstation/ $(TOOLS)/gen-messages.py --messages=$< > $@

generated/settings.h: config/settings.xml $(TOOLS)/gen-settings.py
	@echo GENERATE $@
	$(Q)PYTHONPATH=../groundstation/ $(TOOLS)/gen-settings.py --settings=$< > $@

generated/build.h: $(SRC) $(TOOLS)/gen-build-info.py
	@echo GENERATE $@
	$(Q)PYTHONPATH=../groundstation/ $(TOOLS)/gen-build-info.py --target=$(TARGET) > $@

# Create final output files (.hex, .eep) from ELF output file.
# TODO: handling the .eeprom-section should be redundant
$(OBJDIR)/%.hex: $(OBJDIR)/%.elf
	@echo OBJC $@
	$(Q)$(OBJCOPY) -O $(FORMAT) $< $@

# Create extended listing file from ELF output file.
# testing: option -C
$(OBJDIR)/%.lss: $(OBJDIR)/%.elf
	@echo OBJD $@
	$(Q)$(OBJDUMP) -h -S -C $< > $@

# Create a symbol table from ELF output file.
$(OBJDIR)/%.sym: $(OBJDIR)/%.elf
	@echo NM $@
	$(Q)$(NM) -n $< > $@

# Link: create ELF output file from object files.
.SECONDARY : $(OBJDIR)/$(TARGET).elf
.PRECIOUS : $(AOBJARM) $(COBJARM)
$(OBJDIR)/%.elf:  $(AOBJARM) $(COBJARM)
	@echo LD $@
	$(Q)$(CC) $(THUMB) $(CFLAGS) $(AOBJARM) $(COBJARM)  --output $@ $(LDFLAGS)

# Compile: create object files from C source files. ARM-only
$(OBJDIR)/%.o : %.c
	@echo CC $@
	$(Q)test -d $(dir $@) || mkdir -p $(dir $@)
	$(Q)$(CC) -c $(CFLAGS) $< -o $@ 

# Assemble: create object files from assembler source files. ARM-only
$(AOBJARM) : $(OBJDIR)/%.o : %.S
	@echo AS $@
	$(Q)test -d $(dir $@) || mkdir -p $(dir $@)
	$(Q)$(CC) -c $(ASFLAGS) $< -o $@

clean:
	$(REMOVE) $(OBJDIR)/$(TARGET).hex
	$(REMOVE) $(OBJDIR)/$(TARGET).obj
	$(REMOVE) $(OBJDIR)/$(TARGET).elf
	$(REMOVE) $(OBJDIR)/$(TARGET).map
	$(REMOVE) $(OBJDIR)/$(TARGET).obj
	$(REMOVE) $(OBJDIR)/$(TARGET).a90
	$(REMOVE) $(OBJDIR)/$(TARGET).sym
	$(REMOVE) $(OBJDIR)/$(TARGET).lnk
	$(REMOVE) $(OBJDIR)/$(TARGET).lss
	$(REMOVE) $(OBJDIR)/.depend
	$(REMOVE) $(COBJARM)
	$(REMOVE) $(AOBJARM)
	$(REMOVE) $(LST)
	$(REMOVE) generated/*.h

# Listing of phony targets.
.PHONY : all size build elf hex lss sym clean upload

# Dependencies
$(OBJDIR)/.depend:
	@echo DEPEND $@
	@test -d $(OBJDIR) || mkdir -p $(OBJDIR)
	$(Q)$(CC) -MM -MG $(CFLAGS) $(SRC) | sed 's|\([^\.]*\.o\)|$(OBJDIR)/\1|' > $@

ifneq ($(MAKECMDGOALS),clean) 
ifneq ($(MAKECMDGOALS),erase) 
-include $(OBJDIR)/.depend
endif
endif
