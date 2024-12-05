#!/usr/bin/env python
# This script is the entry point for the simulation.
# It creates a DataFrame with the parameters for the simulation
import pandas as pd
import numpy as np
def main():
    rng = np.random.default_rng(1000)
    num_replicates = 5
    # Genetic architecture scenario
    # Mutation rate (unscaled)
    mu = np.repeat(1e-8, num_replicates)
    # Recombination rate (unscaled)
    rho = np.repeat(1e-8, num_replicates)
    # X mutations are conditionally adaptive
    # Target X value
    target_x = rng.integers(40, 70, size=num_replicates)
    # Migration rate (1%)
    migration = rng.uniform(0.005, 0.01, size=num_replicates)
    # Selection coefficient for Deleterious mutations  
    s_d = np.abs(rng.normal(5e-4, 1e-3, size=num_replicates))
    # Selection coefficient for Conditionally adaptive mutations in p1     
    s_c1 = np.abs(rng.normal(5e-2, 1e-3, size=num_replicates)     )
    # Selection coefficient for Conditionally adaptive mutations in p2
    s_c2 = s_c1
    # Epistasis interaction term in p1
    epsilon1 = np.repeat(0.0, num_replicates)
    # Epistasis interaction term in p2
    epsilon2 = np.repeat(0.0, num_replicates)
    # We model *only* mutations in coding regions
    # (although mutation rate is given including those)
    # Fraction of synonymous mutations in coding regions
    fraction_s = np.repeat(0.309, num_replicates)
    # Fraction of delterious non-synonymous
    fraction_d = rng.uniform(0.45, 0.600, size=num_replicates)
    # During a period of time, we allow some of the mutations to be conditionally adaptive
    # the fraction of mutations that are conditionally adaptive is fraction_c
    # After mutations target X are observed, all nonsynonymous mutations are
    # deleterious (fraction_d + fraction_c)
    fraction_c = 1-fraction_s-fraction_d
    # Inversion parameters
    # genomic length
    L = np.repeat(11e6, num_replicates).astype(int)
    # Inversion length
    inv_length = np.repeat(1e7, num_replicates).astype(int)
    # Demographic parameters
    # Linear-scaling factor of the simulation
    scaling = np.repeat(10, num_replicates)
    # Carrying capacity of population K1
    K1 = np.repeat(20_000 / scaling, num_replicates).astype(int)
    # Carrying capacity of population K2
    K2 = np.repeat(20_000 / scaling, num_replicates).astype(int)
    # Burn-in period (number of generations)
    burnin = (K1*2).astype(int)
    # Max number of generations
    max_runtime = burnin + K1
    # Enabling logging
    logging = 0           

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
        "SCALING": scaling,
        "RHO" : rho,
        "MU": mu,
        "SCALING": scaling,
        "RHO": rho,
        # Demographic parameters
        "K1": K1,
        "K2": K2,
        "MIGRATION": migration,
        "BURNIN": burnin,
        "RUNTIME": max_runtime,
        "LOGGING": logging,
        # Replicates
        "SEED" : [1000+i for i in range(num_replicates)]
    }
    df = pd.DataFrame(data)
    df.to_csv("/dev/stdout", index=False)

if __name__ == "__main__":
    main()
