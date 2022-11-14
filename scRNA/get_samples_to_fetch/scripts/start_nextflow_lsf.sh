#!/usr/bin/env bash

# activate Nextflow conda env
conda init bash
eval "$(conda shell.bash hook)"
conda activate nextflow

# run nextflow main.nf with inputs and lsf config:
export NXF_OPTS="-Xms5G -Xmx5G"
nextflow run nextflow_ci -profile sanger -c inputs.nf --nf_ci_loc $PWD -resume
