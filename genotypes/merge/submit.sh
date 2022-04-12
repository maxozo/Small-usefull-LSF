t='merge'
bsub -R'select[mem>40000] rusage[mem=40000]' -J $t  -n 15 -M 40000 -o $t.o -e $t.e -q long bash ./run.sh \
    /lustre/scratch123/hgi/projects/bhf_finemap/imputation/blueprint/vcf_hg38/sortedhg38_vcfblueprint_wp10_phase2_Concat.vcf.gz \
    /lustre/scratch123/hgi/projects/bhf_finemap/imputation/uk10k_1000g_phase3/vcf_hg38/hg38_uk10k_1000g_phase3_Concat.vcf.gz \
    /lustre/scratch123/hgi/projects/bhf_finemap/imputation/uk10k_1000g_blueprint