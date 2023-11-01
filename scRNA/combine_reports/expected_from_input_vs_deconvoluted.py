
import pandas as pd
import os
import glob
# This code merges all the reports in on file. 
print('lets combine reports')
# Here we produce 2 files: 
# 1) The input samples with their associated pulls
# 2) all the deconvoluted successfully sample ids.

all_vcfs = glob.glob(f'/lustre/scratch123/hgi/projects/cardinal_analysis/qc/*/Summary_plots/Fetch Pipeline/Input/input_table.tsv')

all_samples ={}
count=0
All_Deconvoluted=pd.DataFrame()
All_Deconvoluted_merged=pd.DataFrame()
for path in all_vcfs:
    print(path)
    Tr1 = path.split('/')[-5]
    Tranche_Details = pd.read_csv(f'/lustre/scratch123/hgi/projects/cardinal_analysis/qc/{Tr1}/Summary_plots/Summary/{Tr1}_Tranche_Report.tsv',sep='\t')
    Tranche_Details = Tranche_Details.set_index('Pool id')
    Data = pd.read_csv(path,sep='\t')
    Deconvoluted_Reports = pd.read_csv(f'/lustre/scratch123/hgi/projects/cardinal_analysis/qc/{Tr1}/Summary_plots/Summary/{Tr1}_Donor_Report.tsv',sep='\t')
    DR1 = Deconvoluted_Reports[['Pool ID','Vacutainer ID','Match Expected']]
    All_Deconvoluted = pd.concat([All_Deconvoluted,DR1])
    
    for i,rw1 in Data.iterrows():
        experiment_id = rw1['experiment_id']
        samples = rw1['donor_vcf_ids'].replace('\'','').split(',')
        
        try:
            library_id = Tranche_Details.loc[experiment_id,'Chromium channel number']
        except:
            d2 = pd.read_csv(f'/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/fetch/{Tr1}/results/yascp_inputs/Extra_Metadata.tsv',sep='\t')
            d2 = d2.set_index('experiment_id')
            library_id = d2.loc[experiment_id,'chromium_channel']
        
        Deconvoluted_Reports.loc[Deconvoluted_Reports['Pool ID']==experiment_id,'Chromium channel number']=library_id
        for s1 in samples:
            all_samples[count]={'experiment_id':experiment_id,'library_id':library_id, 'sample':s1}
            count+=1
        print(i)
    All_Deconvoluted_merged = pd.concat([All_Deconvoluted_merged,Deconvoluted_Reports])
All_Samples_Expected = pd.DataFrame(all_samples).T
GEM_BATCHED = pd.read_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/analysis/mo11/files/meta_data.tsv',sep='\t')
GEM_BATCHED = GEM_BATCHED.set_index('Library Plate')
GEM_BATCHED = GEM_BATCHED.reset_index()
All_Deconvoluted_merged['Chromium_channel'] = All_Deconvoluted_merged['Chromium channel number'].str.replace(':','_').str[:-1]
All_Deconvoluted_merged = All_Deconvoluted_merged.set_index('Chromium_channel')
All_Deconvoluted_merged = All_Deconvoluted_merged.reset_index()
All_Deconvoluted_merged['Batch']=''
for i, row1 in GEM_BATCHED.iterrows():
    print(i)
    lp = row1['Library Plate']
    bach = row1['Batch']
    try:
        All_Deconvoluted_merged.loc[All_Deconvoluted_merged['Chromium_channel']==lp,'Batch']=bach
    except:
        print('not yet sequenced')
All_Deconvoluted_merged.to_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/analysis/mo11/files/All_Deconvoluted_merged.tsv',sep='\t')
