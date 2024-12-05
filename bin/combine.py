#!/usr/bin/env python
# This script collects the parameters for the simulation and the simulation results
# and combines them into a single CSV file.
import pandas as pd
import sys
def main(params: str, results: str):
    # First, read the parameters
    params = pd.read_csv(params)
    # Next, read the results and combine them
    # Important: results are assumed to be in the same order as the parameters
    col_names = params.columns
    res = []
    for (theta, outfile) in zip(params.itertuples(), results):
        theta = theta[1:] # Skip the index
        sim = pd.read_csv(outfile)
        for key, val in zip(col_names, theta):
            sim[key] = val
        res.append(pd.DataFrame(sim))
    df = pd.concat(res, ignore_index=True)
    df.to_csv("/dev/stdout", index=False)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])

