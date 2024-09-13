import pandas as pd
import os
import glob
outdir = '/lustre/scratch127/humgen/teams/hgi/mo11/tmp_projects127/cardinal_ukbb_return/purePools_ukbb_donors_return/'

Donor_Report = pd.read_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/ukbb_handover/reports/2024_05_16/ukbb_pihat_processed/Combined_UKBB_Donor_Report.tsv',sep='\t')
Tranche_Report = pd.read_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/ukbb_handover/reports/2024_05_16/ukbb_pihat_processed/Combined_UKBB_Tranche_Report.tsv',sep='\t')

UKBB_TRANCHES = Tranche_Report[(Tranche_Report['ELGH donors expected in the pool'] == 0) & (Tranche_Report['ELGH donors deconvoluted in the pool'] == 0)]
UKBB_TRANCHES = UKBB_TRANCHES.set_index(UKBB_TRANCHES['Pool id']+'.'+UKBB_TRANCHES['Experiment id'])

Donor_Report = Donor_Report.set_index(Donor_Report['Pool ID']+'.'+Donor_Report['Experiment ID'])
Tranches_Where_There_is_at_least_1_ukb_donor = set(UKBB_TRANCHES.index).intersection(set(Donor_Report.index))
Pools_Where_UKB_Donors_Not_Deconvoluted_or_Dont_pass_QC = set(UKBB_TRANCHES['Pool id'])-(set(Donor_Report.index))

UKBB_DONORS_That_Will_Be_Returned = Donor_Report.loc[list(Tranches_Where_There_is_at_least_1_ukb_donor)]
Tranches_That_Will_Be_Returned = UKBB_TRANCHES.loc[list(Tranches_Where_There_is_at_least_1_ukb_donor)]

UKBB_DONORS_That_Will_Be_Returned.to_csv('/lustre/scratch127/humgen/teams/hgi/mo11/tmp_projects127/cardinal_ukbb_return/purePools_ukbb_donors_return/UKBB_DONORS_That_Will_Be_Returned.tsv',sep='\t')
Tranches_That_Will_Be_Returned.to_csv('/lustre/scratch127/humgen/teams/hgi/mo11/tmp_projects127/cardinal_ukbb_return/purePools_ukbb_donors_return/Tranches_That_Will_Be_Returned.tsv',sep='\t')
# Now for each of these we want to refetch the cellranger datasets
df = pd.DataFrame(glob.glob('/lustre/scratch127/humgen/teams/hgi/mo11/tmp_projects127/cardinal_ukbb_return/purePools_ukbb_donors_return/*'),columns=['col'])

for tr1 in set(Tranches_That_Will_Be_Returned['Experiment id']):
    print(tr1)
    if tr1 != 'Cardinal_46112_Nov_02_2022':
        continue
    # if tr1 == 'Cardinal_46112_Nov_02_2022':
    #     continue
    # if len(df[df.col.str.contains(tr1)])>0:
    #     continue
    All_pools = Tranches_That_Will_Be_Returned[Tranches_That_Will_Be_Returned['Experiment id']==tr1]
    # We open the cellranger irods file and only keep the rows that are containing UKBB only data
    cellranger_irods_objects = pd.read_csv(f'/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/fetch/{tr1}/results/cellranger_irods_objects.csv')
    cellranger_irods_objects = cellranger_irods_objects.set_index('sanger_sample_id')
    ukb_only_irods_objects = cellranger_irods_objects.loc[All_pools['Pool id']]
    ukb_only_irods_objects = ukb_only_irods_objects.reset_index()


    
    # We triger the refetch data code
    # os.mkdir(outdir+tr1)
    # ukb_only_irods_objects.to_csv(outdir+tr1+'/cellranger_irods_objects.csv',index=False)
    # os.system(f'cd {outdir+tr1} && python ../../refetch_data.py')
    
    # Now we copy over all the required h5ad files and the associated metadata for each of these 
    # all donors in this tranche
    Tranche_UKBB_DONORS_That_Will_Be_Returned = UKBB_DONORS_That_Will_Be_Returned[UKBB_DONORS_That_Will_Be_Returned['Experiment ID']==tr1]
    for i,tr_donor1 in Tranche_UKBB_DONORS_That_Will_Be_Returned.iterrows():
        print(tr_donor1)
        donor_id = tr_donor1['Pool_ID.Donor_Id'].replace("_don",".don")
        path_to_copy_tsv = f"/lustre/scratch123/hgi/projects/cardinal_analysis/freezes/freeze2/{tr_donor1['Experiment ID']}/Donor_Quantification/{tr_donor1['Pool ID']}/{donor_id}.tsv"
        path_to_copy_h5ad = f"/lustre/scratch123/hgi/projects/cardinal_analysis/freezes/freeze2/{tr_donor1['Experiment ID']}/Donor_Quantification/{tr_donor1['Pool ID']}/{donor_id}.h5ad"
        tf = f'{donor_id}.tsv'
        os.system(f'cd {outdir+tr1+"/"+tr_donor1["Pool ID"]} && bsub -R"select[mem>20000] rusage[mem=20000]" -J cram_{donor_id} -n 1 -M 20000 -o cram_{donor_id}.o -e cram_{donor_id}.e -q normal bash ../../../generate_cram_files.sh {tf} {donor_id} {path_to_copy_tsv} {path_to_copy_h5ad} {tr_donor1["Pool ID"]}')
        
        
    
# For each of these we want to copy the h5ad files
# For each of these we want to split the bam/cram files


print('Done')