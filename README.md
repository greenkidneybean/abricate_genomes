# Abricate for Genomes
_Identify some fun stuff in a slew of genomes_

This is a simple wrapper for [ABRicate](https://github.com/tseemann/abricate) by Torsten Seemann to generate a .csv (please forgive me Torsten) that concatenates all virulence factors found among the eight databases that can be searched with ABRicate.

## Quickstart:
```
git clone https://github.com/greenkidneybean/abricate_genomes.git
cd abricate_genomes
conda create --name abricate_env --file env/abricate_linux.txt
python abricate_genomes.py samples.csv
```

## Setup
1. Clone this repo
```
git clone https://github.com/greenkidneybean/abricate_genomes.git
```
2. Install [Miniconda](https://hpc.nih.gov/apps/python.html)
3. Create the `abricate_env` conda environment:
```
conda create --name abricate_env --file abricate_linux.txt
```

## Input
Takes a .csv file with two columns: "samples" and "path".  Check-out the `samples.csv` file as a guide for formating the sample input.
```
sample,path
sample_1,test/sample_1.fa
sample_2,test/sample_2.fa
sample_3,test/sample_3.fa
```

## Output
The `abricate_genomes.py` file will generate a new directory titled "abricate" containing a pile of files.  The primary output file of interest is the `abricate/abricate.csv`, which flattens the results of each sample `summary.csv` into a single line.  A zero (0) indicates that the virulence factor was not found in any of the eight databases.  A one (1) indicates that the virulence factor was found in **at least** one of the eight databases.
```
abricate
├── abricate.csv                # summary file of virulence factors
├── fig                         # sample heatmaps with database hits
│   ├── sample_1.png
│   ├── sample_2.png
│   └── sample_3.png
└── samples
    ├── sample_1                # database.out for each database
    │   ├── argannot.out
    │   ├── card.out
    │   ├── ecoh.out
    │   ├── ecoli_vf.out
    │   ├── ncbi.out
    │   ├── plasmidfinder.out
    │   ├── resfinder.out
    │   ├── summary.csv         # summary table of percent hit in each database
    │   ├── summary.tab         # summary table of percent hit in each database
    │   └── vfdb.out
    └── ...
```

## Run
```
# activate the "abricate_env" conda environment
conda activate abricate_env

# check the very mild help flag for script options
python abricate_genomes.py -h

# run abricate_genomes.py with the provided test data
python abricate_genomes.py samples.csv
```
