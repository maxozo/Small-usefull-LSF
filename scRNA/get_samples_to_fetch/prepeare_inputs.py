import os
import pandas as pd
from datetime import date
# 9th may, 26th may, ELGH_all, Run_44753 (froxen_fresh)
# Already_Analysed_Files2 = pd.DataFrame(Already_Analysed_Files)
# Already_Analysed_Files2.columns = ['sanger_sample_id']
# Already_Analysed_Files2.to_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/fetch/fech_input_prep/All_Processed',index=False)
Already_Analysed_Files = pd.read_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/fetch/fech_input_prep/All_Processed.tsv')
# Already_Analysed_Files =[
#     "CRD_CMB12813646"
#     ,"CRD_CMB12813647"
#     ,"CRD_CMB12813648"
#     ,"CRD_CMB12813649"
#     ,"CRD_CMB12813650"
#     ,"CRD_CMB12813651"
#     ,"CRD_CMB12813652"
#     ,"CRD_CMB12813653"
#     ,"CRD_CMB12813654"
#     ,"CRD_CMB12813655"
#     ,"CRD_CMB12922397"
#     ,"CRD_CMB12922398"
#     ,"CRD_CMB12922399"
#     ,"CRD_CMB12922400"
#     ,"CRD_CMB12922401"
#     ,"CRD_CMB12922402"
#     ,"CRD_CMB12922403"
#     ,"CRD_CMB12922404"
#     ,"CRD_CMB12922405"
#     ,"ELGH_VAL11509201"
#     ,"ELGH_VAL11509202"
#     ,"ELGH_VAL11509203"
#     ,"ELGH_VAL11509204"
#     ,"ELGH_VAL11509205"
#     ,"ELGH_VAL11509206"
#     ,"ELGH_VAL11509207"
#     ,"ELGH_VAL11650907"
#     ,"ELGH_VAL11650908"
#     ,"ELGH_VAL12156641"
#     ,"ELGH_VAL12156642"
#     ,"ELGH_VAL12156643",
#     'CRD_CMB12813783',
#     'CRD_CMB12813782'
# ]

output_stream = os.popen('imeta qu -z /seq -C study_id = 6776')
data = output_stream.read()
data = pd.DataFrame(data.split('\n'))
d3 = pd.DataFrame(data)
df = data[data[0].str.startswith('collection')]
all_samples = df[0].str.split('/').str[-1].str.split('_').str[3:5].str.join("_")
all_run_ids = df[0].str.split('/').str[-1].str.split('_').str[2]
all_run_ids.index = all_samples
New_Samples = set(all_samples) - set(Already_Analysed_Files['sanger_sample_id'])
if (len(New_Samples)==0):
    print("No new samples")
else:
    print(f"{len(New_Samples)} new samples")
    New_Samples = pd.DataFrame(New_Samples)
    New_Samples.columns = ['sanger_sample_id']
    New_Samples.index = New_Samples['sanger_sample_id']
    New_Samples['Run_ID']= all_run_ids
    All_Processed = pd.DataFrame(set(all_samples).union(set(Already_Analysed_Files['sanger_sample_id'])))
    All_Processed.columns = ['sanger_sample_id']

    for Run_ID1 in set(New_Samples.Run_ID):
        print(Run_ID1)
        today = date.today()
        d4 = today.strftime("%b_%d_%Y")
        New_Samples_Run = New_Samples[New_Samples.Run_ID == Run_ID1]
        New_Samples_Run2 = New_Samples_Run.sanger_sample_id
        os.mkdir(f"/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/fetch/Cardinal_{Run_ID1}_{d4}")
        os.mkdir(f"/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc/Cardinal_{Run_ID1}_{d4}")
        New_Samples_Run2.to_csv(f"/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/fetch/Cardinal_{Run_ID1}_{d4}/input.tsv",index=False)
        os.system(f"cd /lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/fetch/Cardinal_{Run_ID1}_{d4} && git clone -b add_sql_metadata https://github.com/wtsi-hgi/nf_irods_to_lustre.git && bash nf_irods_to_lustre/scripts/nohup_start_nextflow_lsf.sh")
        os.system(f"cd /lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc/Cardinal_{Run_ID1}_{d4} && git clone https://github.com/wtsi-hgi/yascp.git")
        
        os.system('cp /lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/fetch/fech_input_prep/All_Processed.tsv /lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/fetch/fech_input_prep/Backup_All_Processed.tsv')
    All_Processed.to_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/fetch/fech_input_prep/All_Processed.tsv',index=False)