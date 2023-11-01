import pandas as pd
import os
import glob

print('lets combine reports')


all_vcfs = glob.glob(f'/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc/*/results_rsync2/results/handover/Summary_plots/*/Fetch Pipeline/CSV/Submission_Data_Pilot_UKB.file_metadata.tsv')
All_Tranche_Data = []

for tr1 in all_vcfs:
    print(tr1)
    path2 = '/'.join(tr1.split('/')[:-7])
    tranche_id = path2.split('/')[-2]
    D1 = pd.read_csv(tr1,sep='\t')
    for sample1 in D1['Sample_id']:
        print(sample1)
        nr_cr_cells = int(D1[D1['Sample_id']==sample1]['Estimated Number of Cells'].values[0].replace(',',''))
        f2 = glob.glob(f'{path2}/results/nf-preprocessing/cellbender/{sample1}/cellbender-epochs_*/cellbender-FPR_0pt1-filtered_10x_mtx/barcodes.tsv.gz')
        for f123 in f2:
            D2 = pd.read_csv(f123)
            nr_cb_cells = len(D2)
            All_Tranche_Data.append({'tranche_id':tranche_id,'pool_id':sample1,'CR cells':nr_cr_cells,'CB cells':nr_cb_cells})
            
cell_number_comparisons = pd.DataFrame(All_Tranche_Data) 

cell_number_comparisons.to_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/analysis/mo11/compare_cellranger_and_cellbender_cell_nrs/cell_number_comparisons.tsv',sep='\t')
print('Done')