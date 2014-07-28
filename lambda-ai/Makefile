ICFP_BASE := $(CURDIR)/../
LISPC := $(ICFP_BASE)/gcc/gcc-lispc
AS := $(ICFP_BASE)/gcc/gcc-as

all: main.gcc

main.gcc: ai.s asm.S

ai.s: .FORCE

%.s: %.lambda
	$(LISPC) $< > $@

%.gcc: %.s
	$(AS) $< > $@

%.paste: %.gcc
	cat $^ | xclip -selection c -i

main.gcc:
	$(AS) $^ > $@

clean:
	rm -f *.s *.gcc

.FORCE:
