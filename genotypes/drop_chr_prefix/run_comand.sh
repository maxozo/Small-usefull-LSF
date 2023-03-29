# cc=$1
# zcat /lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/onek1k/topmed_imputed/maf_filter/chr"$cc"_R2_0.3_MAF_0.0001.vcf.gz | awk '{gsub(/^chr/,""); print}' | awk '{gsub(/ID=chr/,"ID="); print}' > no_prefix_chr"$cc"_R2_0.3_MAF_0.0001.vcf
# bgzip no_prefix_chr"$cc"_R2_0.3_MAF_0.0001.vcf
# bcftools index no_prefix_chr"$cc"_R2_0.3_MAF_0.0001.vcf.gz

# zcat /lustre/scratch123/hgi/teams/hgi/mo11/tmp_projects/harriet/sarek/genotype/joint_germline_recalibrated.vcf.gz | awk '{gsub(/^chr/,""); print}' | awk '{gsub(/ID=chr/,"ID="); print}' > /lustre/scratch123/hgi/teams/hgi/mo11/tmp_projects/harriet/sarek/genotype/no_prefix_chr_joint_germline_recalibrated.vcf.gz
# bgzip /lustre/scratch123/hgi/teams/hgi/mo11/tmp_projects/harriet/sarek/genotype/no_prefix_chr_joint_germline_recalibrated.vcf.gz
bcftools index /lustre/scratch123/hgi/teams/hgi/mo11/tmp_projects/harriet/sarek/genotype/no_prefix_chr_joint_germline_recalibrated.vcf.gz