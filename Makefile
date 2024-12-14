IMAGE = environment.sif
DEF_FILE = environment.def
SCRIPT = analysis.nf

# Target to build the image
$(IMAGE): $(DEF_FILE)
	apptainer build --fakeroot $(IMAGE) $(DEF_FILE)

env: $(IMAGE)

run: $(IMAGE) $(SCRIPT)
	./$(SCRIPT) -qs 40 -resume -with-apptainer $(IMAGE) --config=scenarios/low_x_scenario_no_recomb_inv.yaml --source=model_no_recomb_inv.slim
	./$(SCRIPT) -qs 40 -resume -with-apptainer $(IMAGE) --config=scenarios/low_x_scenario_no_recomb.yaml --source=model.slim
	./$(SCRIPT) -qs 40 -resume -with-apptainer $(IMAGE) --config=scenarios/low_x_scenario.yaml --source=model.slim
	./$(SCRIPT) -qs 40 -resume -with-apptainer $(IMAGE) --config=scenarios/high_x_scenario.yaml --source=model.slim
