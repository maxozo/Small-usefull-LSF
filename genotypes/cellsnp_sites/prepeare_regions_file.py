import pandas as pd
CellSnP = pd.read_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc/genome1K.phase3.SNP_AF5e2.chr1toX.hg38.vcf.gz',sep='\t', skiprows=234) 
Subset = CellSnP[['#CHROM','POS']] 
Subset['#CHROM'] = 'chr'+Subset['#CHROM'].astype(str)
# Subset['Regions_File'] = Subset['#CHROM'].astype(str)+':'+Subset['POS'].astype(str)
Regions = Subset['Regions_File'] 
Regions.to_csv('/lustre/scratch123/hgi/projects/bhf_finemap/random/genotypes/cellsnp_sites/CellSNP_subset.tsv',sep='\t',index=False,header=False)
# chr1:59040
print('Done')