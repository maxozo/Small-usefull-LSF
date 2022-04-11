# bcftools annotate -x INFO,^FORMAT/GT,FORMAT/AF $1 -Oz --threads 5 -o $2
# bcftools index vcf/*.vcf.gz
bcftools concat /lustre/scratch123/hgi/projects/bhf_finemap/imputation/uk10k_1000g_phase3/vcfs/*vcf.gz -Oz --threads 15 -o  /lustre/scratch123/hgi/projects/bhf_finemap/imputation/uk10k_1000g_phase3/vcfs/merged/uk10k_1000g_phase3_Concat.vcf.gz
