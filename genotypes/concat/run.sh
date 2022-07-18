# bcftools annotate -x INFO,^FORMAT/GT,FORMAT/AF $1 -Oz --threads 5 -o $2
# bcftools index vcf/*.vcf.gz
bcftools concat /lustre/scratch123/hgi/projects/ukbiobank_genotypes/FullRelease/Imputed/VCFs/hg38_bcf/*bcf.gz -Ob --threads 6 -o  /lustre/scratch123/hgi/projects/ukbiobank_genotypes/FullRelease/Imputed/VCFs/concat/hg38_ukbb_Concat_basement.bcf.gz
