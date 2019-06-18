#!/usr/bin/env python

"""
This script requires a samples.csv file with two columns.

Column 1 - sample name
Column 2 - full path to genome

Output - "abricate" directory,
    - sub-directory for each sample
    - summary.tsv
"""

import argparse
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

parser = argparse.ArgumentParser() #description='Run Abricate against genomes'
"""parser.add_argument('input', type=str,
                   help='samples.csv file')
parser.add_argument("-o", "--output", type=str, default='abricate',
                   help='output directory path (default: ./abricate/)')
"""
parser.add_argument("input", type=str,
                    help="samples.csv input file")
parser.add_argument("--output", type=str, default='abricate',
                    help="output directory path (default: ./abricate/)")
args = parser.parse_args()

# set input/output
sample_file = args.input
out = args.output

# import samples.tsv
samples = pd.read_csv(sample_file, header=0)

# list of abricate databases
abricate_db = [
    'argannot',
    'card',
    'ecoh',
    'ecoli_vf',
    'ncbi',
    'plasmidfinder',
    'resfinder',
    'vfdb'
    ]

# dictionary to concat all results
samples_dict = {}

# run abricate
for item, row in samples.iterrows():
    sample = row['sample']
    genome = row['path']
    output = f'{out}/samples/{sample}'

    # make abricate output folder
    if not os.path.exists(output):
        os.makedirs(output)

    # abricate results for each database
    for database in abricate_db:
        cmd = f'abricate --db {database} {genome} > {output}/{database}.out'
        os.system(cmd)

    # concat abricate results
    summary_file = f"{output}/summary.tab"
    cmd = f'abricate --summary {output}/*.out > {output}/summary.tab'
    os.system(cmd)

    # create .csv
    df = pd.read_csv(summary_file, delimiter='\t')
    df.replace('.', 0, inplace=True)

    def fix_this(x):
        value = str(x)
        if ';' in value:
            value = value.split(';')[0]
        #value = float(value)
        return value
    for i in df.columns:
        df[i] = df[i].apply(fix_this)

    # make figs
    # shorten the column names to 20 characters
    cols = list(df.columns)
    new_cols = [x[:20] for x in cols]
    df.columns = new_cols
    float_cols = list(df.columns)[2:]
    for i in float_cols:
        df[i] = df[i].astype('float')
    df.set_index('#FILE', inplace=True)

    # figure path
    fig_out = f'{out}/fig'
    if not os.path.exists(fig_out):
        os.makedirs(fig_out)

    # save heatmapt to "fig" folder
    plt.figure(figsize=(15,4))
    ax = sns.heatmap(df[df.columns[1:]], cmap='viridis')
    plt.title(sample)
    plt.tight_layout()
    ax.figure.savefig(f'{fig_out}/{sample}.png')

    # switch back to long column names
    df.columns = cols[1:]
    df.to_csv(f'{output}/summary.csv')

    temp_dict = {key:1 for key in df.columns.tolist()[1:]}
    samples_dict[sample] = temp_dict

# concat all data
df = pd.DataFrame(samples_dict)
df = df.transpose()
df.replace(np.nan, 0, inplace=True)
df.to_csv(f'{out}/abricate.csv')
