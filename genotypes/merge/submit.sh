t='merge'
bsub -R'select[mem>20000] rusage[mem=20000]' -J $t  -n 15 -M 20000 -o $t.o -e $t.e -q long bash ./run.sh \
    /lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/filtered_genotypes/vcf/merged_bcf/GT_AF_ELGH_Concat.bcf.gz \
    /lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/1000G_full_GRCh38_sorted_chrAdded.vcf.gz \
    /lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes \
    ELGH_1000g