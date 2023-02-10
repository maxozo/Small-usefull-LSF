library(data.table)
# flip strand
tofix = fread("/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/topmed_imputations/onek1k/Prep_TOPMed_server/snps-excluded.txt", header=T, sep = "\t", fill = T)
names(tofix)[1] = "Position"
table(tofix$FilterType)
bim = fread("/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/topmed_imputations/onek1k/Feb28k_autosome_maf0.01_geno0.01_excPalindromic_SNPonly.bim")
bim[, Position := paste0("chr",V1,":",V4,":",V6,":",V5)]
all(tofix$Position %in% bim$Position)
tofix = merge(bim, tofix, by = "Position")
tofixstrand = tofix[grep("Strand flip", FilterType),]
fwrite(tofixstrand[,.(V2)], "/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/topmed_imputations/onek1k/Prep_TOPMed_server/SNPs_Strand_Flip.txt", col.names = F)

# Typed-only SNPs
typedonly = fread("/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/topmed_imputations/onek1k/Prep_TOPMed_server/typed-only.txt", header = T)
names(typedonly)[1] = "Position"
all(typedonly$Position %in% bim$Position)
fwrite(bim[Position %in% typedonly$Position,.(V2)], "/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/topmed_imputations/onek1k/Prep_TOPMed_server/SNPs_Typed_only.txt", col.names = F)
