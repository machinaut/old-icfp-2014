ICFP_BASE := $(CURDIR)/../
LISPC := $(ICFP_BASE)/gcc/gcc-lispc
AS := $(ICFP_BASE)/gcc/gcc-as

all: ai.gcc

%.s: %.lambda
	$(LISPC) $^ > $@

%.gcc: %.s
	$(AS) $^ > $@

clean:
	rm -f *.s *.gcc
