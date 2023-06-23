# This code combines all the diferent panels in one cellsnp file

# ukb panel
bcftools concat /lustre/scratch125/humgen/teams/hgi/mo11/ukb/hg38_ft_MAF_0pt0001_INFO_coding/cellsnp_panel/*.vcf.gz -Oz -o \
/lustre/scratch125/humgen/teams/hgi/mo11/ukb/hg38_ft_MAF_0pt0001_INFO_coding/combined_cellsnp_panel/combined_cellsnp_pos.vcf.gz
bcftools index /lustre/scratch125/humgen/teams/hgi/mo11/ukb/hg38_ft_MAF_0pt0001_INFO_coding/combined_cellsnp_panel/combined_cellsnp_pos.vcf.gz

# elgh R1 panel
bcftools concat /lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/ELGH/release1/topmed_imputed/maf_INFO_filter_coding/cellsnp_panel/*.vcf.gz -Oz -o \
/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/ELGH/release1/topmed_imputed/maf_INFO_filter_coding/combined_cellsnp_panel/combined_cellsnp_pos.vcf.gz
bcftools index /lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/ELGH/release1/topmed_imputed/maf_INFO_filter_coding/combined_cellsnp_panel/combined_cellsnp_pos.vcf.gz

# elgh R3_4 panle

bcftools concat /lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/ELGH/release34/hg38_ft_MAF_0pt0001_INFO_coding/cellsnp_panel/*.vcf.gz -Oz -o \
/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/ELGH/release34/hg38_ft_MAF_0pt0001_INFO_coding/combined_cellsnp_panel/combined_cellsnp_pos.vcf.gz
bcftools index /lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/ELGH/release34/hg38_ft_MAF_0pt0001_INFO_coding/combined_cellsnp_panel/combined_cellsnp_pos.vcf.gz

# Merge al the data together
bcftools merge \
/lustre/scratch125/humgen/teams/hgi/mo11/ukb/hg38_ft_MAF_0pt0001_INFO_coding/combined_cellsnp_panel/combined_cellsnp_pos.vcf.gz \
/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/ELGH/release1/topmed_imputed/maf_INFO_filter_coding/combined_cellsnp_panel/combined_cellsnp_pos.vcf.gz \
/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/ELGH/release34/hg38_ft_MAF_0pt0001_INFO_coding/combined_cellsnp_panel/combined_cellsnp_pos.vcf.gz \
/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/putative_celline/sorted_fixref_1kgAF05.U937Thp1.h38.coding.vcf.gz \
-Oz -o /lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/cellsnp_panel/merged_sites_UKB_ELGH_Celline1kg_MAF0pt01_INFO_0pt9.vcf.gz

# Info on all the sites:
# UKBB: 355300
# ELGH R1: 198414
# ELGH R3_4: 187327
# CellSNP: 273004

# TOTAL: 628495

