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

def simple_investigation():
    adata1 ='/lustre/scratch123/hgi/mdt1/projects/jaguar_analysis/analysis/mo11/sample_yascp_run/4.yascp_full_run1.5/results/clustering/normalize=total_count.vars_to_regress=pct_counts_gene_group__mito_transcript/reduced_dims-null-harmony.n_pcs=19.variables=experiment_id.thetas=1.0/umap_gather_out_gene_symbols.h5ad'
    ad1 = sc.read_h5ad(filename=adata1)
    # donor_ids = [f'pool1.donor{i}' for i in range(12)]
    # donor_filtered_adata = ad1[ad1.obs['Pool.Donor'].isin(donor_ids)]
    # donor_filtered_adata.write(
    #     '/software/hgi/pipelines/QTLight/test_Onek1kPool1.h5ad',
    #     compression='gzip'
    # )
    sc.pl.violin(ad1, ['n_genes_by_counts', 'total_counts', 'pct_counts_gene_group__mito_transcript'],
             jitter=0.4, multi_panel=True)
    

def look_at_whether_all_samples_are_present():
    #  Purpose - sometimes the reports have a missing samples. Therefore to restart pipeline its good to look at whether this info is in the file in first place.
    adata1 ='/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc/Cardinal_46499_Jan_21_2023/results/merged_h5ad/outlier_filtered_adata.h5ad'
    ad1 = sc.read_h5ad(filename=adata1)
    print('Done')
    lane_qc = ad1.obs[ad1.obs['convoluted_samplename']=='ELGH_VAL12156641']
    Donor_data = lane_qc[lane_qc['Donor'] == 'donor1']
    
    

    #     'convoluted_samplename', 'donor_id', 'prob_max', 'prob_doublet',
    #    'n_vars', 'best_singlet', 'best_doublet', 'experiment_id',
    #    'chromium_channel', 'id_run', 'id_study_tmp', 'id_study_lims',
    #    'last_updated', 'loading_concentration', 'created', 'instrument_model',
    #    'instrument_external_name', 'instrument_name', 'n_pooled', 'instrument',
    #    'nr_ukbb_samples', 'nr_elgh_samples', 'nr_spikeins', 'n_cells',
    #    'n_genes_by_counts', 'log1p_n_genes_by_counts', 'total_counts',
    #    'log1p_total_counts', 'pct_counts_in_top_50_genes',
    #    'pct_counts_in_top_100_genes', 'pct_counts_in_top_200_genes',
    #    'pct_counts_in_top_500_genes',
    #    'total_counts_gene_group__mito_transcript',
    #    'log1p_total_counts_gene_group__mito_transcript',
    #    'pct_counts_gene_group__mito_transcript',
    #    'total_counts_gene_group__mito_protein',
    #    'log1p_total_counts_gene_group__mito_protein',
    #    'pct_counts_gene_group__mito_protein',
    #    'total_counts_gene_group__ribo_protein',
    #    'log1p_total_counts_gene_group__ribo_protein',
    #    'pct_counts_gene_group__ribo_protein',
    #    'total_counts_gene_group__ribo_rna',
    #    'log1p_total_counts_gene_group__ribo_rna',
    #    'pct_counts_gene_group__ribo_rna', 'cell_passes_qc', 'batch',
    #    'log10_ngenes_by_count', 'normalization_factor',
    #    'Azimuth:predicted.celltype.l2', 'Azimuth:predicted.celltype.l2.score',
    #    'Azimuth:mapping.score', 'Azimuth:L0_predicted.celltype.l2',
    #    'Azimuth:L1_predicted.celltype.l2',
    #    'Celltypist:Immune_All_High:predicted_labels',
    #    'Celltypist:Immune_All_High:over_clustering',
    #    'Celltypist:Immune_All_High:majority_voting',
    #    'Celltypist:Immune_All_Low:predicted_labels',
    #    'Celltypist:Immune_All_Low:over_clustering',
    #    'Celltypist:Immune_All_Low:majority_voting', 'Donor', 'Exp',
    #    'cell_passes_hard_filters',
    #    'cell_passes_qc-per:Azimuth:L0_predicted.celltype.l2',
    #    'cell_passes_qc-per:Azimuth:L0_predicted.celltype.l2:score',
    #    'cell_passes_qc:score', 'cell_passes_qc-per:all_together::exclude',
    #    'cell_passes_qc-per:all_together::exclude:score'],
# look_at_whether_all_samples_are_present()
# compare_merge_methods()
simple_investigation()
print('Done')



