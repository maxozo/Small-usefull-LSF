#!/usr/bin/env python


__date__ = '2022-07-20'
__version__ = '0.0.1'
import os
import pandas as pd
from datetime import date
import argparse



"""Run CLI."""
parser = argparse.ArgumentParser(
    description="""
        Place all the files in the correct places.
        """
)

parser.add_argument(
    '-i', '--input',
    dest='input',
    required=False,
    default='test',
    help='Input mode'
)

options = parser.parse_args()
type_of_run = options.input
# type_of_run='run'
# This code runs the imeta querry and determines which files have already been run. 
# It further creates required folders in each of the analysis folders - 
# i.e:
# 1) Fech folder
# 2) QC folder
# 3) Cardinal Analysis folder

# type_of_run='test' #please changet this to 'run' to process samples.
Already_Analysed_Files = pd.read_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/fetch/SETUP_fech_input_prep/All_Processed.tsv')

# Querry irods for all the available runs
output_stream = os.popen('imeta qu -z /seq -C study_id = 6776')
data = output_stream.read()
data = pd.DataFrame(data.split('\n'))
d3 = pd.DataFrame(data)
df = data[data[0].str.startswith('collection')]
all_samples = df[0].str.split('/').str[-1].str.split('_').str[3:5].str.join("_")
all_run_ids = df[0].str.split('/').str[-1].str.split('_').str[2]
all_run_ids.index = all_samples

# Check all the new samples

New_Samples = set(all_samples) - set(Already_Analysed_Files['sanger_sample_id'])

if type_of_run=='test':
    # For TEST purposes we are just picking the first available 3 samples
    New_Samples = all_samples[1:4]

if (len(New_Samples)==0):
    print("No new samples")
else:
    print(f"{len(New_Samples)} new samples")
    New_Samples = pd.DataFrame(New_Samples)
    New_Samples.columns = ['sanger_sample_id']
    New_Samples.index = New_Samples['sanger_sample_id']
    New_Samples['Run_ID']= all_run_ids
    if type_of_run=='test':
        # for TEST run we just make the run as a random digit 
        New_Samples['Run_ID']= 'TEST_12345'
    else:
        #  if this is not a test case we want ot update a file where we list whats already processed.
        All_Processed = pd.DataFrame(set(all_samples).union(set(Already_Analysed_Files['sanger_sample_id'])))
        All_Processed.columns = ['sanger_sample_id']
        All_Processed.to_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/fetch/SETUP_fech_input_prep/All_Processed.tsv',index=False)
    
    for Run_ID1 in set(New_Samples.Run_ID):
        today = date.today()
        d4 = today.strftime("%b_%d_%Y")
        print("##########################")
        # if this is not a test case and multiple new runs have been deposited to IRODS we want to split them out in a different Tranches
        print(f"Have set up a directory structure for Cardinal_{Run_ID1}_{d4} and trigerred the Fech run at: \n 1) /lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/fetch/Cardinal_{Run_ID1}_{d4} \n When this is completed please triger qc step in: \n 2) /lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc/Cardinal_{Run_ID1}_{d4}")
        print(f"To do this please run - \n 3) cd /lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc/Cardinal_{Run_ID1}_{d4} && bash ./scripts/nohup_start_nextflow_lsf.sh")
        print("##########################\n")

        New_Samples_Run = New_Samples[New_Samples.Run_ID == Run_ID1]
        New_Samples_Run2 = New_Samples_Run.sanger_sample_id
        os.mkdir(f"/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/fetch/Cardinal_{Run_ID1}_{d4}")
        os.mkdir(f"/lustre/scratch123/hgi/projects/cardinal_analysis/qc/Cardinal_{Run_ID1}_{d4}")
        os.mkdir(f"/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc/Cardinal_{Run_ID1}_{d4}")
        New_Samples_Run2.to_csv(f"/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/fetch/Cardinal_{Run_ID1}_{d4}/input.tsv",index=False)
        os.system(f"cd /lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/fetch/Cardinal_{Run_ID1}_{d4} && git clone -b add_sql_metadata https://github.com/wtsi-hgi/nf_irods_to_lustre.git && bash nf_irods_to_lustre/scripts/nohup_start_nextflow_lsf.sh")
        os.system(f"cd /lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc/Cardinal_{Run_ID1}_{d4} && git clone https://github.com/wtsi-hgi/yascp.git")
        os.system(f"cp -r /lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/fetch/SETUP_fech_input_prep/scripts /lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc/Cardinal_{Run_ID1}_{d4}")
        os.system(f"cp /lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/fetch/SETUP_fech_input_prep/inputs.nf /lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc/Cardinal_{Run_ID1}_{d4}")
        # for backup purposes we keep the samples already analysed in a different directory.
        os.system(f'cp /lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/fetch/SETUP_fech_input_prep/All_Processed.tsv /lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/fetch/SETUP_fech_input_prep/{d4}_Backup_All_Processed.tsv')
