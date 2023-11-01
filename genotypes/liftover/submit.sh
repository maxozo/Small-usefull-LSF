bsub -R'select[mem>40000] rusage[mem=40000]' -J liftover  -n 3 -M 40000 -o liftover.o -e liftover.e -q long bash ./run_bed.sh \
    /lustre/scratch123/hgi/projects/bhf_finemap/summary_stats/1M_Hearts/with_chr_CHD_meta_SAIGE_complete_filtered_30.1.19.bed \
    CHD_meta_SAIGE_complete_filtered_30 \
    /lustre/scratch123/hgi/projects/bhf_finemap/summary_stats/1M_Hearts