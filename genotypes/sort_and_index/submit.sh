bsub -R'select[mem>40000] rusage[mem=40000]' -J sort2  -n 5 -M 40000 -o sort2.o -e sort2.e -q long bash ./run.sh \
    /lustre/scratch123/hgi/projects/bhf_finemap/imputation/uk10k_1000g_phase3/vcf_hg38/hg38_uk10k_1000g_phase3_Concat.vcf.gz \
    hg38_uk10k_1000g_phase3_Concat \
    /lustre/scratch123/hgi/projects/bhf_finemap/imputation/uk10k_1000g_phase3/vcf_hg38