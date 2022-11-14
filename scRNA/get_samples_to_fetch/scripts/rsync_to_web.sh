#!/usr/bin/env bash
# run this script as this bash rsync_to_web.sh project_name
# /volume/scRNA_test_app/scrna_static_and_media_files/bin
# rsync -vr ./results/handover/Summary_plots/* ubuntu@172.27.22.139:/volume/scRNA_test_app/scrna_static_and_media_files/media/$1
export LC_HGI_USER=mercury
# rsync -vr Summary_plots/* ubuntu@172.27.22.139:/volume/scRNA_test_app/scrna_static_and_media_files/media/$1
# for d in Summary_plots/* ; do
#     part2=$(basename "$d")
#     echo "$part2"
#     rsync -vrL Summary_plots/$part2/* /lustre/scratch123/hgi/projects/cardinal_analysis/qc/$part2/Summary_plots 
#     rsync -vrL  ../../../results/handover/Donor_Quantification /lustre/scratch123/hgi/projects/cardinal_analysis/qc/$part2/
#     rsync -vrL Summary_plots/$part2/Summary/Extra_Metadata_Donors.tsv /lustre/scratch123/hgi/projects/cardinal_analysis/qc/$part2/Donor_Quantification/
#     rsync -vrL "./Summary_plots/$part2/GT Match___1000/assignments_all_pools.tsv" /lustre/scratch123/hgi/projects/cardinal_analysis/qc/$part2/Donor_Quantification/
# done

