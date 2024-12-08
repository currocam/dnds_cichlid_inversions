#!/usr/bin/env python
# This script is the entry point for the simulation.
# It creates a DataFrame with the parameters for the simulation
import pandas as pd
import numpy as np
def main():
    rng = np.random.default_rng(1000)
    num_replicates = 1000
    # Genetic architecture scenario
    # Mutation rate (unscaled)
    mu = np.repeat(1e-7, num_replicates)
    # Recombination rate (unscaled)
    rho = np.repeat(1e-7, num_replicates)
    # X mutations are conditionally adaptive
    # Target X value
    target_x = rng.uniform(70, 120, size=num_replicates).astype(int)
    # Migration rate
    migration = rng.uniform(0.001, 0.01, size=num_replicates)
    # Selection coefficient for Deleterious mutations  
    s_d = rng.uniform(0.001, 0.005, size=num_replicates)
    # Selection coefficient for Conditionally adaptive mutations in p1     
    s_c1 = rng.uniform(0.001, 0.005, size=num_replicates)
    # Selection coefficient for Conditionally adaptive mutations in p2
    s_c2 = rng.uniform(0.001, 0.005, size=num_replicates)
    # Epistasis interaction term in p1
    epsilon1 = rng.choice([0.0, 1.0], size=num_replicates) * (-1 / target_x)
    # Epistasis interaction term in p2
    epsilon2 = 1 / target_x
    # We model *only* mutations in coding regions
    # (although mutation rate is given including those)
    # Fraction of synonymous mutations in coding regions
    fraction_s = np.repeat(0.309, num_replicates)
    # Fraction of delterious non-synonymous
    fraction_d = np.repeat(0.600, num_replicates)
    # During a period of time, we allow some of the mutations to be conditionally adaptive
    # the fraction of mutations that are conditionally adaptive is fraction_c
    # After mutations target X are observed, all nonsynonymous mutations are
    # deleterious (fraction_d + fraction_c)
    fraction_c = 1-fraction_s-fraction_d
    # Inversion parameters
    # genomic length
    # Inversion length
    inv_length = rng.uniform(5e6, 1e7, size=num_replicates).astype(int)
    L = (inv_length+1e6).astype(int)
    # Demographic parameters
    # Population size of population 1 and 2
    N1 = N2 = rng.uniform(1000, 5000, size=num_replicates).astype(int)
    # Initial population size of population 2
    init_n2 = (N2*rng.uniform(0, 0.5, size=num_replicates)).astype(int)
    # Growth rate of population 2
    alpha = rng.uniform(0.01, 0.1, size=num_replicates)
    # Burn-in period (number of generations)
    burnin = (4*N1).astype(int)
    # Max number of generations
    max_runtime = (7*N1).astype(int)
    # Enabling logging
    logging = np.repeat(0, num_replicates)

    # Create CSV with hyperparameters
    data = {
        # Genetic architecture
        "TARGET_X": target_x,
        "s_D" : s_d,
        "s_C1": s_c1,
        "s_C2": s_c2,
        "FRACTION_S": fraction_s,
        "FRACTION_D": fraction_d,
        "FRACTION_C": fraction_c,
        "epsilon1": epsilon1,
        "epsilon2": epsilon2,
        # Inversion parameters
        "L" : L,
        "INV_LENGTH": inv_length,
        # Genetic parameters
        "RHO" : rho,
        "MU": mu,
        "RHO": rho,
        # Demographic parameters
        "N1": N1,
        "N2": N2,
        "ALPHA": alpha,
        "INIT_N2": init_n2,
        "MIGRATION": migration,
        "BURNIN": burnin,
        "RUNTIME": max_runtime,
        "LOGGING": logging,
        # Replicates
        "SEED" : [1000+i for i in range(num_replicates)]
    }
    # Check that all parameters are the same length
    assert all(len(v) == num_replicates for v in data.values())
    df = pd.DataFrame(data)
    df.to_csv("/dev/stdout", index=False)

if __name__ == "__main__":
    main()

