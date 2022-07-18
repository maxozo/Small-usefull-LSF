sample='hg38_ukb_imp_chrX_v3'
bsub -R'select[mem>80000] rusage[mem=80000]' -J $sample/sort -n 5 -M 80000 -o sort_$sample.o -e sort_$sample.e -q basement bash ./run.sh \
   /lustre/scratch123/hgi/projects/ukbiobank_genotypes/FullRelease/Imputed/VCFs/hg38_bcf/sex_chr/hg38_ukb_imp_chrX_v3.bcf.gz \
    $sample \
    /lustre/scratch123/hgi/projects/ukbiobank_genotypes/FullRelease/Imputed/VCFs/hg38_bcf_sorted
    