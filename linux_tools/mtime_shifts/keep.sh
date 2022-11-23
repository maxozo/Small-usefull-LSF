#!/usr/bin/env bash
set -e

declare -a tokeep=(
    "/lustre/scratch123/hgi/mdt1/projects/ukbb_scrna/pipelines/Pilot_UKB/deconv/franke_data_postcellbender"
)
    #declare -a tokeep=(
    #"/lustre/scratch123/hgi/mdt1/projects/ukbb_scrna/pipelines/Pilot_UKB/qc/ELGH_nfCore"
    #"/lustre/scratch123/hgi/mdt1/projects/ukbb_scrna/pipelines/Pilot_UKB/qc/Superloading_Exp_nfCore"
    #"/lustre/scratch123/hgi/mdt1/projects/ukbb_scrna/pipelines/Pilot_UKB/qc/Deconvolution_Exp4_nfCore"
    #"/lustre/scratch123/hgi/mdt1/projects/ukbb_scrna/pipelines/Pilot_UKB/fetch/42603__ELGH_CardVal"
    #"/lustre/scratch123/hgi/mdt1/projects/ukbb_scrna/pipelines/Pilot_UKB/fetch/ELGH" )

for i in "${tokeep[@]}"
do
    echo loop: "$i"
    find $i -type f -exec bash -c "echo \"{}\" >> tokeep.fofn  " \;
done
