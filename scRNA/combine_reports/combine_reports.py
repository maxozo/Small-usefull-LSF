import pandas as pd
import os
import glob
# This code merges all the reports in on file. 
print('lets combine reports')



All_Tranche_Data = pd.DataFrame()
UKBB_Reports = pd.DataFrame()
UKBB_Missing = pd.DataFrame()
UKBB_Not_Expected = pd.DataFrame()
all_vcfs = glob.glob(f'/lustre/scratch123/hgi/projects/cardinal_analysis/qc/*/Summary_plots')
for path in all_vcfs:
    print(path)
    Tranche_name = path.split('/')[-2]
    Tranche_Data = pd.read_csv(f'{path}/Summary/{Tranche_name}_Tranche_Report.tsv',sep='\t')
    try:
        Donor_Data = pd.read_csv(f'{path}/Summary/UKBB_REPORT/{Tranche_name}_UKBB_Report.tsv',sep='\t')
        Donor_Metadata = pd.read_csv(f'/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/fetch/{Tranche_name}/results/yascp_inputs/Extra_Metadata_Donors.tsv',sep='\t')
        Donor_Metadata['Pool_ID']=Donor_Metadata['experiment_id'].str.split('__').str[0]
        Donor_Metadata['matched_donor_id']=Donor_Metadata['Pool_ID']+'__'+Donor_Metadata['donor']
        Donor_Metadata = Donor_Metadata.drop_duplicates(subset=['matched_donor_id'])
        Donor_Metadata = Donor_Metadata.set_index('matched_donor_id')
        Donor_Data['Vacutainer ID']=Donor_Data['Vacutainer ID'].astype(str)
        Donor_Data['matched_donor_id']=Donor_Data['Pool ID']+'__'+Donor_Data['Vacutainer ID']
        
        Donor_Data = Donor_Data.set_index('matched_donor_id')
        Donor_Metadata.drop_duplicates()
        Donor_Data['Sequencing time']=Donor_Metadata['State']
        Donor_Data['PBMC extraction date']=Donor_Metadata['PBMC extraction date']
        UKBB_Reports = pd.concat([UKBB_Reports,Donor_Data])
        try:
            Missing_Donors = pd.read_csv(f'{path}/Summary/UKBB_REPORT/{Tranche_name}_Missing_UKBB_Donors.tsv',sep='\t')
            UKBB_Missing = pd.concat([UKBB_Missing,Missing_Donors])
        except:
            print('no missing')
        try:
            Not_Expected = pd.read_csv(f'{path}/Summary/UKBB_REPORT/{Tranche_name}_Not_Expected_UKBB_Donors.tsv',sep='\t')
            UKBB_Not_Expected = pd.concat([UKBB_Not_Expected,Not_Expected])
        except:
            print('no missing')
    except:
        print(f'{Tranche_name} doesnt contain UKBB reports')
    All_Tranche_Data = pd.concat([All_Tranche_Data,Tranche_Data])
    print('path')
    
    
All_Tranche_Data.to_csv('/lustre/scratch123/hgi/projects/cardinal_analysis/analysis/mo11/combined_reports/01_23_combined_reports/Combined_UKBB_Tranche_Report.tsv',sep='\t',index=False)    
UKBB_Reports.to_csv('/lustre/scratch123/hgi/projects/cardinal_analysis/analysis/mo11/combined_reports/01_23_combined_reports/Combined_UKBB_Donor_Report.tsv',sep='\t',index=False)
UKBB_Not_Expected.to_csv('/lustre/scratch123/hgi/projects/cardinal_analysis/analysis/mo11/combined_reports/01_23_combined_reports/Combined_UKBB_Not_Expected.tsv',sep='\t',index=False)
UKBB_Missing.to_csv('/lustre/scratch123/hgi/projects/cardinal_analysis/analysis/mo11/combined_reports/01_23_combined_reports/Combined_UKBB_Missing.tsv',sep='\t',index=False)
    
    
    
    
    