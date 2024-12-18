#!/usr/bin/env python
import numpy as np
import pandas as pd
import re, sys

def extract_expected_ratios(path: str) -> dict:
    data_pattern = re.compile(r"##<N/S=(?P<ns>[-+]?\d*\.\d+|\d+),D/S=(?P<ds>[-+]?\d*\.\d+|\d+)>")
    with open(path, 'r') as file:
        line = next(file)
        while line.startswith("##"):
            match = data_pattern.match(line)
            if match:
                return {
                    "N/S": float(match.group("ns")),
                    "D/S": float(match.group("ds"))
                }
            line = next(file)    
    raise ValueError("No valid line with the pattern '#<N/S=value,D/S=value>' found.")
    
# Define the left, right, and center bins for the analysis later
def widening_bins(bin_width):
    right_bins = np.concatenate([
        1 - np.arange(bin_width, 1+bin_width, bin_width),
        np.repeat(1, 1//bin_width+2)
    ])
    left_bins = np.concatenate([
        np.repeat(-1, 1//bin_width+1),
        0 + np.arange(0.0, 1+bin_width, bin_width),
    ])
    midpoints = np.arange(-1, 1+bin_width, bin_width)  
    return left_bins, right_bins, midpoints

def main(infile):
    bin_width = 0.05
    sites_df = pd.read_csv(infile, comment='#', names=["Pearson", "Type"])
    expected_ratios = extract_expected_ratios(infile)
    sites_df["Pearson"] = (sites_df["Pearson"].to_numpy()).astype(float)
    sites_df["classification"] = np.where(sites_df.Type == "MutationType<m2>", "Synonymous", "Non-synonymous")
    sites_df = sites_df.dropna()
    left_bins, right_bins, midpoints = widening_bins(bin_width)
    res = {
        "r_bin" : [],
        "Synonymous" : [],
        "Non-synonymous" : [],
    }
    for left, right, midpoint in zip(left_bins, right_bins, midpoints):
        mask = (sites_df["Pearson"] > left) & (sites_df["Pearson"] <= right)
        res["r_bin"].append(midpoint)
        masked_df = sites_df[mask]
        res["Synonymous"].append((masked_df["classification"] == "Synonymous").sum())
        res["Non-synonymous"].append((masked_df["classification"] == "Non-synonymous").sum())
    df = pd.DataFrame(res)
    df["expected_dNdS"] = expected_ratios["N/S"]
    df["dNdS"] = (df["Non-synonymous"] / df["Synonymous"]) / expected_ratios["N/S"]
    # Count how many times the inversion was lost and add it as a new column
    with open(infile, 'r') as file:
        n_lost = sum(1 for line in file if "Inversion was lost" in line)
    df["n_lost"] = n_lost
    df.to_csv("/dev/stdout", index=False)
    
if __name__ == "__main__":
    main(sys.argv[1])