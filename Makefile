IMAGE = environment.sif
DEF_FILE = environment.def
SCRIPT1 = analysis_dnds.nf
SCRIPT2 = analysis_strength.nf

# Run all scenarios
run: $(IMAGE) $(SCRIPT)
	./$(SCRIPT1) -qs 40 -resume -with-apptainer $(IMAGE) --config=scenarios/high_x.yaml --source=model.slim
	./$(SCRIPT1) -qs 40 -resume -with-apptainer $(IMAGE) --config=scenarios/low_x.yaml --source=model.slim
	./$(SCRIPT1) -qs 40 -resume -with-apptainer $(IMAGE) --config=scenarios/low_x_no_epistasis.yaml --source=model.slim
	./$(SCRIPT1) -qs 40 -resume -with-apptainer $(IMAGE) --config=scenarios/high_x_no_epistasis.yaml --source=model.slim
	./$(SCRIPT2) -resume -with-apptainer $(IMAGE) --config=scenarios/high_x_strength.yaml --source=model_strength.slim
	./$(SCRIPT2) -resume -with-apptainer $(IMAGE) --config=scenarios/low_x_strength.yaml --source=model_strength.slim

# Target to build the image
$(IMAGE): $(DEF_FILE)
	apptainer build --fakeroot $(IMAGE) $(DEF_FILE)

# Convenience target to build the environment
env: $(IMAGE)
	@echo "Apptainer environment image is ready: $(IMAGE)"