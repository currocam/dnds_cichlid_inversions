#!/usr/bin/env python
# This script is the entry point for the simulation.
# It creates a DataFrame with the parameters for the simulation

import pandas as pd
import numpy as np
import yaml, sys

def main(infile):
    # Load constants from a YAML file
    with open(infile, "r") as file:
        constants = yaml.safe_load(file)
    
    rng = np.random.default_rng(constants["seed"])
    num_replicates = constants["num_replicates"]

    # Load parameters from the YAML file
    mu = np.repeat(constants["mu"], num_replicates)
    rho = np.repeat(constants["rho"], num_replicates)
    target_x = rng.uniform(*constants["target_x_range"], size=num_replicates).astype(int)
    migration = rng.uniform(*constants["migration_range"], size=num_replicates)
    s_d = rng.uniform(*constants["s_d_range"], size=num_replicates)
    s_c1 = rng.uniform(*constants["s_c1_range"], size=num_replicates)
    s_c2 = rng.uniform(*constants["s_c2_range"], size=num_replicates)
    epsilon1 = [rng.uniform(*x, size=num_replicates) if len(x) > 1 else np.repeat(x, num_replicates) for x in constants["epsilon1"]]
    epsilon1 = [np.random.choice(x) for x in np.array(epsilon1).T] / target_x
    epsilon2 = [rng.uniform(*x, size=num_replicates) if len(x) > 1 else np.repeat(x, num_replicates) for x in constants["epsilon2"]] / target_x
    epsilon2 = [np.random.choice(x) for x in np.array(epsilon2).T]
    fraction_s = np.repeat(constants["fraction_s"], num_replicates)
    fraction_n = np.repeat(constants["fraction_n"], num_replicates)
    inv_length = np.repeat(constants["inv_length"], num_replicates).astype(int)
    L = (inv_length + constants["inv_offset"]).astype(int)
    N1 = N2 = rng.uniform(*constants["n_range"], size=num_replicates).astype(int)
    init_n2 = (N2 * rng.uniform(*constants["init_n2_range"], size=num_replicates)).astype(int)
    alpha = rng.uniform(*constants["alpha_range"], size=num_replicates)
    burnin = (4 * N1).astype(int)
    max_runtime = (burnin + constants["max_runtime"]).astype(int)
    waiting_time = np.repeat(constants["waiting_time"], num_replicates)
    logging = np.repeat(constants["logging"], num_replicates)

    # Create CSV with hyperparameters
    data = {
        "TARGET_X": target_x,
        "s_D": s_d,
        "s_C1": s_c1,
        "s_C2": s_c2,
        "FRACTION_S": fraction_s,
        "FRACTION_N": fraction_n,
        "epsilon1": epsilon1,
        "epsilon2": epsilon2,
        "L": L,
        "INV_LENGTH": inv_length,
        "RHO": rho,
        "MU": mu,
        "N1": N1,
        "N2": N2,
        "ALPHA": alpha,
        "INIT_N2": init_n2,
        "MIGRATION": migration,
        "BURNIN": burnin,
        "RUNTIME": max_runtime,
        "WAITING": waiting_time,
        "LOGGING": logging,
        "SEED": [constants["seed"] + i for i in range(num_replicates)],
    }

    assert all(len(v) == num_replicates for v in data.values())
    df = pd.DataFrame(data)
    df.to_csv("/dev/stdout", index=False)

if __name__ == "__main__":
    main(sys.argv[1])
