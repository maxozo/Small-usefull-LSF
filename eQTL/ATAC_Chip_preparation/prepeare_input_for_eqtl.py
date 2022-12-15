import pandas as pd
from gtfparse import read_gtf

Data1 = pd.read_csv('/lustre/scratch123/hgi/projects/macromap/ATAC/results/bwa/mergedLibrary/macs/narrowPeak/consensus/consensus_peaks.mLb.clN.featureCounts.txt',sep='\t', comment='#',)
Data_Analysis = Data1.rename(columns={'Geneid':'gene_id'})
Data_Analysis.columns = Data_Analysis.columns.str.replace('.mLb.clN.bam','')
Data_Analysis = Data_Analysis.drop(columns=['Chr','Start','End','Strand','Length'])
# 'gene_id','start','end','strand','seqname'
Data_Analysis.insert(1,'gene_name','')
Data_Analysis['gene_name']="Chr_"+Data1['Chr'].astype(str)+";Start:"+Data1['Start'].astype(str)+";End:"+Data1['End'].astype(str)
gtf_file = Data1[['Geneid','Chr','Start','End','Strand','Length']]
gtf_file = gtf_file.rename(columns={'Geneid':'gene_id','Chr':'seqname','Start':'start','End':'end','Strand':'strand'})
print('Done')
gtf_file.to_csv('/lustre/scratch123/hgi/projects/macromap/ATAC/eQTLs/atac_gtf_input.tsv',sep='\t',index=False)
Data_Analysis.to_csv('/lustre/scratch123/hgi/projects/macromap/ATAC/eQTLs/atac_phenotype_input.tsv',sep='\t',index=False)