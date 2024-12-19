#!/usr/bin/env python
# This script is the entry point for the simulation.
# It creates a DataFrame with the parameters for the simulation

import pandas as pd
import numpy as np
import yaml, sys
import numpy as np
from scipy.optimize import fsolve


def process_input(rng, value, size):
    if isinstance(value, (str)):
        value = float(value)
    if isinstance(value, (int, float)):
        # Repeat the number 'size' times
        return np.repeat(value, size)
    elif isinstance(value, list) and len(value) == 2:
        # Draw 'size' samples from a uniform distribution
        low, high = value
        return rng.uniform(low, high, size)
    else:
        raise ValueError("Input must be a single number or a list of two numbers.")

# Adjust additive effect and epistasis term
def fitness(args, x):
  sc, eps = args[0], args[1]
  het = (1+sc)**x * (1+eps)**(x*(x-1)/2)
  hom = (1+sc)**(2*x) * (1+eps)**(2*x*(2*x-1)/2)
  return np.array([het, hom])

def solve_terms(target_het, target_hom, x): 
  def fn(args):
    return fitness(args, x) - np.array([target_het, target_hom])
  return fsolve(fn, [0, 0])

def main(infile):
    # Load constants from a YAML file
    with open(infile, "r") as file:
        constants = yaml.safe_load(file)
    
    rng = np.random.default_rng(constants["seed"])
    target_het_fitness = np.repeat(constants["target_het_fitness"], constants["num_replicates"])
    target_hom_fitness = np.repeat(constants["target_hom_fitness"], constants["num_replicates"])
    assert len(target_het_fitness) == len(target_hom_fitness)
    num_replicates =  len(target_het_fitness)
    process = lambda x : process_input(rng, x, num_replicates)
    # Load parameters from the YAML file
    mu = process(constants["mu"])
    rho = process(constants["rho"])
    target_x = process(constants["target_x"]).astype(int)
    migration = process(constants["migration_range"])
    s_d = process(constants["s_d"])
    terms = [solve_terms(het, hom, x) for het, hom, x in zip(target_het_fitness, target_hom_fitness, target_x)]
    s_c1 = s_c2 = [sol[0] for sol in terms]
    epsilon1 = epsilon2 = [sol[1] for sol in terms]
    fraction_s = process(constants["fraction_s"])
    fraction_n =  process(constants["fraction_n"])
    inv_length = process(constants["inv_length"]).astype(int)
    L = (inv_length + constants["inv_offset"]).astype(int)
    N1 = N2 = process(constants["n_range"]).astype(int)
    init_n2 = (N2 * process(constants["init_n2_range"])).astype(int)
    alpha =process(constants["alpha_range"])
    burnin = (4 * N1).astype(int)
    max_runtime = (burnin + process(constants["max_runtime"])).astype(int)
    waiting_time = (N2 * process(constants["waiting_time"])).astype(int)
    logging = process(constants["logging"])
    # Create CSV with hyperparameters
    data = {
            "TARGET_X": target_x,
            "fitness_heterozygous": target_het_fitness,
            "fitness_homozygous": target_hom_fitness,
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
