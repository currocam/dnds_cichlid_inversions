#!/usr/bin/env python
# This script does the heavy parsing of the parameters from the CSV
# and generates the command line arguments for SLiM execution
import pandas as pd
import sys
def main(infile):
    infile = pd.read_csv(infile)
    columns = infile.columns
    for row in infile.itertuples():
        values = row[1:]
        cmd = ['slim', '-l', '0', '-t', '-m']
        for val, col in zip(values, columns):
            if col == 'SEED':
                cmd.append(f"-s {val}")
                continue
            # Convert value into a representation that SLiM can understand. 
            # Make sure that integers are not converted to floats
            if pd.isna(val):
                continue
            cmd.append("-d")
            cmd.append(f"{col}={val}")
        print(" ".join(cmd))

if __name__ == "__main__":
    main(sys.argv[1])

