# bcftools annotate -x INFO,^FORMAT/GT,FORMAT/AF $1 -Oz --threads 5 -o $2
# bcftools index vcf/*.vcf.gz
bcftools concat /nfs/team151_data02/BluePrint_data/wp10/wp10_phase2_2017/2017_QTL_SUMMARY_STATISTICS/../GENOTYPE/*vcf.gz -Oz --threads 15 -o  /lustre/scratch123/hgi/projects/bhf_finemap/imputation/blueprint/vcfblueprint_wp10_phase2_Concat.vcf.gz
