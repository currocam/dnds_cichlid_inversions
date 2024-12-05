IMAGE = environment.sif
DEF_FILE = environment.def
SCRIPT = analysis.nf
# Target to build the image
$(IMAGE): $(DEF_FILE)
	apptainer build --fakeroot $(IMAGE) $(DEF_FILE)
env : $(IMAGE)

run: $(IMAGE) $(SCRIPT)
	./$(SCRIPT) -resume -with-apptainer $(IMAGE)
