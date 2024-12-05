#!/usr/bin/env python
# This script analyzes a VCF file produced by SLiM to produce the dN/dS ratio data
# It is highly coupled to the specific parametrization of the the simulation
import numpy as np
import pandas as pd
from scipy.stats import pearsonr
from typing import Tuple
import io, sys

# Parse the VCF file into a pandas DataFrame
def read_vcf(path: str) -> pd.DataFrame:
    with open(path, 'r') as f:
        lines = [l for l in f if not l.startswith('##')]
    return pd.read_csv(
        io.StringIO(''.join(lines)),
        dtype={'#CHROM': str, 'POS': int, 'ID': str, 'REF': str, 'ALT': str,
               'QUAL': str, 'FILTER': str, 'INFO': str},
        sep='\t'
    ).rename(columns={'#CHROM': 'CHROM'})

# Extract information about the SNPs and convert variable names into a more human-readable format
def extract_site_info(df_vcf: pd.DataFrame) -> pd.DataFrame:
    mutations = pd.DataFrame({
        "positions": df_vcf.POS.to_numpy(),
        "mut_type": df_vcf['INFO'].str.extract(r'\bMT=(\d+)').astype(int).to_numpy().reshape(-1)
    })
    mutation_mapping = {
        1: "Neutral (non-coding)", 2: "Neutral (coding)", 3: "Deleterious",
        4: "Conditionally adaptive", 5 : "Start inversion", 6: "End inversion"
    }
    classification_mapping = {
        1: np.nan, 2: "Synonymous", 3: "Non-synonymous",
        4: "Non-synonymous", 5 : np.nan, 6: np.nan
    }
    mutations["classification"] = [classification_mapping[x] for x in mutations["mut_type"].to_numpy()]
    mutations["mut_type"] = [mutation_mapping[x] for x in mutations["mut_type"].to_numpy()]
    return mutations
# Extract the haplotypes from the VCF, as well as an indicator variable for whether
# the individual was sampled from p1 or p2
def extract_haplotypes(df_vcf: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
    sample_columns = [col for col in df_vcf.columns if col.startswith('i')]
    population_indicator, haplotypes = [], []
    for i in [0, 1]:
        # We have the same number of individuals of eahc population
        population_indicator.append(np.zeros(len(sample_columns)//2))
        population_indicator.append(np.ones(len(sample_columns)//2))
        haplotypes.append(np.array(
            [df_vcf[ind].str.split('|').str[0].values.astype(np.int32) for ind in sample_columns]
        ))
    return np.concatenate(population_indicator), np.concatenate(haplotypes)

# Define the left, right, and center bins for the analysis later
def widening_bins(bin_width: float)-> Tuple[np.ndarray, np.ndarray, np.ndarray]:
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


def analysis(df_vcf: pd.DataFrame, bin_width: float)->pd.DataFrame:
    sites_df = extract_site_info(df_vcf)
    population_indicator, haplotypes = extract_haplotypes(df_vcf)
    # Exclude non-variable sites
    mask = haplotypes.var(axis=0) > 0
    sites_df= sites_df[mask]
    haplotypes= haplotypes[:, mask]
    # Compute Pearson correlations
    r_vector = np.array([
            pearsonr(population_indicator, snp_states).statistic for snp_states in haplotypes.T
        ])
    sites_df["r"] = r_vector
    # Drop non-coding sites and dummy markers
    sites_df = sites_df.dropna()
    # Compute number of Synonymous, Non-synonymous sites and deleterious Non-synonymous sites
    left_bins, right_bins, midpoints = widening_bins(bin_width)
    res = {
        "r_bin" : [],
        "Synonymous" : [],
        "Non-synonymous" : [],
        "Deleterious" : []
    }
    for left, right, midpoint in zip(left_bins, right_bins, midpoints):
        mask = (sites_df["r"] > left) & (sites_df["r"] <= right)
        sites_df.loc[mask, "bin"] = midpoint
        res["r_bin"].append(midpoint)
        masked_df = sites_df[mask]
        res["Synonymous"].append((masked_df["classification"] == "Synonymous").sum())
        res["Non-synonymous"].append((masked_df["classification"] == "Non-synonymous").sum())
        res["Deleterious"].append((masked_df["mut_type"] == "Deleterious").sum())
    return pd.DataFrame(res)

def main(infile: str)-> None:
    df_vcf = read_vcf(infile)
    bin_width = 0.1
    res = analysis(df_vcf, bin_width)
    res.to_csv("/dev/stdout", index=False)

if __name__ == "__main__":
    main(sys.argv[1])

