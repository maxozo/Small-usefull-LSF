import pandas as pd
idx1=''
idx2=''
Data1 = pd.read_csv('/lustre/scratch123/hgi/teams/hgi/mo11/tmp/tobi/blood/fech/results/yascp_inputs/pre_Extra_Metadata.tsv',sep='\t')
Data2 = pd.read_csv('/lustre/scratch123/hgi/teams/hgi/mo11/tmp/tobi/full_analysis/GUT_scRNAseq_metadata - GUT_scRNAseq-cleaned.csv',sep=',')
Data1 = Data1.set_index('experiment_id')
Data2 = Data2.set_index('sanger_sample_id')
D3 = Data2.loc[Data1.index]
Overlap = set(Data2.index).intersection(set(Data1.index))
Distinct = set(Data1.index)-set(Data2.index)
result = pd.concat([Data1, D3], axis=1)
result.to_csv('/lustre/scratch123/hgi/teams/hgi/mo11/tmp/tobi/blood/fech/results/yascp_inputs/Extra_Metadata.tsv',sep='\t')
print('Done')
