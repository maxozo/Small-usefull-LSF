import pandas as pd
CellSnP = pd.read_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc/genome1K.phase3.SNP_AF5e2.chr1toX.hg38.vcf',sep='\t', skiprows=234) 
Subset = CellSnP[['#CHROM','POS']] 
Subset['#CHROM'] = 'chr'+Subset['#CHROM'].astype(str)
Subset.to_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/CellSnP_subset.tsv',sep='\t',index=False,header=False)
print('Done')