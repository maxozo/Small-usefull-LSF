import pandas as pd


D1 = pd.read_csv('/lustre/scratch123/hgi/teams/hgi/mo11/tmp/huvec/ATAC/results/samples/study_id_6946/samples_noduplicates.tsv',sep='\t',index=1)
D2 = pd.read_csv('/lustre/scratch123/hgi/projects/bhf_finemap/random/rnaseq/fastq_preprocess/Run_HUVEC_ATAC.csv',sep='\t',index=1)



print('Done')