import scanpy as sc
import pandas as pd

def compare_merge_methods():
    # Purpose - check the matches between merged ad file and presplit - Tobi asked if I can add the layers int the logp1 layer in a merged ad file - the way to do it to add it to the batch split and then pass it to the combination script. 
    adata1 ='/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc/Blood_Fresh/results_rsync_exclude2/results/merged_h5ad/pre_QC_adata.h5ad'
    adata2 ='/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc/Blood_Fresh/results_hard_filters/merged_h5ad/pre_QC_adata.h5ad'

    ad1 = sc.read_h5ad(filename=adata1)
    ad2 = sc.read_h5ad(filename=adata2)
    df1 = ad1.to_df()
    df2 = ad2.to_df()
    comparison = df1.compare(df2)
    print('Done')

def look_at_whether_all_samples_are_present():
    #  Purpose - sometimes the reports have a missing samples. Therefore to restart pipeline its good to look at whether this info is in the file in first place.
    adata1 ='/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc/Cardinal_46291_Nov_29_2022/results_rsync2/results/merged_h5ad/pre_QC_adata.h5ad'
    ad1 = sc.read_h5ad(filename=adata1)
    print('Done')



compare_merge_methods()
print('Done')



