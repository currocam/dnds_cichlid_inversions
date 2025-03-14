# Simulations of selection on inversion haplotypes
[![DOI](https://zenodo.org/badge/898630257.svg)](https://doi.org/10.5281/zenodo.14930226)

## Overview

TO-DO: Add from the main text 

## Reproducibility

You can build the container by executing `make env` if you have apptainer installed. 

```
apptainer --version
make env
```

You can execute the different analyses by executing `make` if Nextflow is installed. 

```
nextflow -version
make
```

## Project structure

The necessary scripts to (1) draw different combinations of parameters, (2) execute the SLiM model with the appropriate flags and (3) parse the resulting tables are located in the `bin` directory. Orchestrating the different processes is done with Nextflow scripts located at the project's root. SLiM models are also located at the root of the project. 

## Parameters

The parameters are specified in YAML files. These files are located in the `scenarios` directory. We presented two scenarios when analyzing the dN/dS ratio. 

- [X=100. A high number of conditionally adaptive sites to perform the dN/dS analysis](scenarios/high_x.yaml) 
- [X=2. A low number of conditionally adaptive sites to perform the dN/dS analysis. ](scenarios/low_x.yaml)

The allele fitness effects were chosen so that an individual in the derived population that is homozygous for all conditionally adaptive sites would have ~60% higher fitness than an individual with the same deleterious mutations but none of the adaptive. 

We also studied how the number of conditionally adaptive loci affected the frequency with which the inversions were lost. We simulated data for both scenarios and four levels of total strength of selection: 

- [X=100. A high number of conditionally adaptive sites to study how often the inversions are lost.](scenarios/high_x_strength.yaml) 
- [X=2. A low number of conditionally adaptive sites to study how often the inversions are lost.](scenarios/low_x_strength.yaml)

As a "bonus" (as we did not observe differences), we did some preliminary analysis setting the epistasis term to zero. 

- [X=100. A high number of conditionally adaptive sites without epistasis to explore its effect on dN/dS.](scenarios/high_x_no_epistasis.yaml)
- [X=2. A high number of conditionally adaptive sites without epistasis to explore its effect on dN/dS.](scenarios/low_x_strength.yaml)

