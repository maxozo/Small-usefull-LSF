import glob
import pandas as pd

all_dons = []
all_samples = glob.glob('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/fetch/*/results/yascp_inputs/input.tsv')
for input_file in all_samples:
    _=''
    tranche = input_file.split('/')[-4]
    Data = pd.read_csv(input_file,sep='\t')
    for i,r1 in Data.iterrows():
        print(i)
        Donors = r1.donor_vcf_ids.replace("'",'').split(',')
        for don in Donors:
            all_dons.append({'Tranche_name':tranche,'idx':r1.experiment_id,'donor':don})
            
all_donors_processed = pd.DataFrame(all_dons)
all_donors_processed.to_csv(f"/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/ukbb_handover/reports/Tengs_Samples/all_samples_total_from_inputs.tsv",sep='\t')
print('Done')