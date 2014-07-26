GCCAS = gcc-as
TARGETS = dfs.gcc

all: $(TARGETS)

%.gcc: %.asm
	$(GCCAS) $< > $@

%.paste: %.asm
	$(GCCAS) $< | xclip -selection c -i

clean:
	rm -rf $(TARGETS)
