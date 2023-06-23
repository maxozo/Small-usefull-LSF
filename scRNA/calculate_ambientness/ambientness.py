
# This code loads each of the quantified datasets and calculates the number of reads removed by cellbender.

import glob
import pandas

import argparse
import scanpy as sc
from typing import Dict
import numpy as np
import tables
from distutils.version import LooseVersion
from typing import Dict
import tables
import scipy
import scipy.io
import scipy.sparse
import gzip
import pandas as pd
import numpy as np
import anndata
import scanpy as sc
import click
import logging
import os

def dict_from_h5(file: str) -> Dict[str, np.ndarray]:
    """Read in everything from an h5 file and put into a dictionary."""
    d = {}
    with tables.open_file(file) as f:
        # read in everything
        for array in f.walk_nodes("/", "Array"):
            d[array.name] = array.read()
    return d

def anndata_from_h5(file: str,analyzed_barcodes_only: bool = True) -> 'anndata.AnnData':
    """Load an output h5 file into an AnnData object for downstream work.

    Args:
        file: The h5 file
        analyzed_barcodes_only: False to load all barcodes, so that the size of
            the AnnData object will match the size of the input raw count
            matrix. True to load a limited set of barcodes: only those
            analyzed by the algorithm. This allows relevant latent
            variables to be loaded properly into adata.obs and adata.obsm,
            rather than adata.uns.

    Returns:
        adata: The anndata object, populated with inferred latent variables
            and metadata.
    """
    d = dict_from_h5(file)
    X = scipy.sparse.csc_matrix(
        (d.pop('data'), d.pop('indices'), d.pop('indptr')),
        shape=d.pop('shape')
    ).transpose().tocsr()

    if analyzed_barcodes_only:
        if 'barcodes_analyzed_inds' in d.keys():
            X = X[d['barcodes_analyzed_inds'], :]
            d['barcodes'] = d['barcodes'][d['barcodes_analyzed_inds']]
        elif 'barcode_indices_for_latents' in d.keys():
            X = X[d['barcode_indices_for_latents'], :]
            d['barcodes'] = d['barcodes'][d['barcode_indices_for_latents']]
        else:
            print(
                'Warning: analyzed_barcodes_only=True, but the key ',
                '"barcodes_analyzed_inds" or "barcode_indices_for_latents" ',
                'is missing from the h5 file. ',
                'Will output all barcodes, and proceed as if ',
                'analyzed_barcodes_only=False'
            )

    print(d.keys())

    # Construct the count matrix.
    if 'gene_names' in d.keys():
        gene_symbols = d.pop('gene_names').astype(str)
    else:
        gene_symbols = d.pop('name').astype(str)
    adata = anndata.AnnData(
        X=X,
        obs={'barcode': d.pop('barcodes').astype(str)},
        var={
            'gene_ids': d.pop('id').astype(str),
            'gene_symbols': gene_symbols,
            'feature_type':d.pop('feature_type').astype(str),
        }
    )
    # adata = adata[:,adata.var.query('feature_type=="Gene Expression"').index]
    adata.obs.set_index('barcode', inplace=True)
    adata.var.set_index('gene_ids', inplace=True)
    
    
    
    # Add other information to the adata object in the appropriate slot.
    for key, value in d.items():
        try:
            value = np.asarray(value)
            if len(value.shape) == 0:
                adata.uns[key] = value
            elif value.shape[0] == X.shape[0]:
                if (len(value.shape) < 2) or (value.shape[1] < 2):
                    adata.obs[key] = value
                else:
                    adata.obsm[key] = value
            elif value.shape[0] == X.shape[1]:
                if value.dtype.name.startswith('bytes'):
                    adata.var[key] = value.astype(str)
                else:
                    adata.var[key] = value
            else:
                adata.uns[key] = value
        except Exception:
            print(
                'Unable to load data into AnnData: ', key, value, type(value)
            )

    if analyzed_barcodes_only:
        cols = adata.obs.columns[
            adata.obs.columns.str.startswith('barcodes_analyzed')
            | adata.obs.columns.str.startswith('barcode_indices')
        ]
        for col in cols:
            try:
                del adata.obs[col]
            except Exception:
                pass

    return adata


# Loop through all the raw files and quantify the ambientness in each of the pools.
all_files = glob.glob("/lustre/scratch123/hgi/projects/cardinal_analysis/qc/*/Donor_Quantification/*/Cellranger_raw_*.h5")

all_ambientness = []

for file1 in all_files:
    print(file1)
    splits = file1.split('/')
    path1 = file1
    tranche = splits[-4]
    pool = splits[-2]

    try:
        adata_cellbender = anndata_from_h5(f'/lustre/scratch123/hgi/projects/cardinal_analysis/qc/{tranche}/Donor_Quantification/{pool}/Cellbender_filtered_0pt1__{pool}.h5',
                                                analyzed_barcodes_only=True)
    except:
        # /lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc/Cardinal_45327_Jul_18_2022/results_rsync2/results/nf-preprocessing/cellbender/CRD_CMB13016570/cellbender-epochs_250__learnrt_0pt000005__zdim_100__zlayer_500__lowcount_10/cellbender_FPR_0.01_filtered.h5
        try:
            adata_cellbender = anndata_from_h5(f'/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc/{tranche}/results_rsync2/results/nf-preprocessing/cellbender/{pool}/cellbender-epochs_250__learnrt_0pt000005__zdim_100__zlayer_500__lowcount_10/cellbender_FPR_0.01_filtered.h5',
                                                analyzed_barcodes_only=True)
        except:
            print('No ambientness association since no cb file exists')
            all_ambientness.append({'pool':pool,'tranche':tranche,'ambientness':None,'Number_of_genes':None,'Number_of_cells':None})
            continue
    adata_cellbender_un = anndata_from_h5(path1,
                                            analyzed_barcodes_only=True)

    # adata_cellbender['TTCATTGGTACCTAAC-1'].X.sum()
    filtered_adata_cellbender_un =  adata_cellbender_un[adata_cellbender.obs.index]

    f3 = filtered_adata_cellbender_un.X - adata_cellbender.X
    Number_of_cells = f3.shape[0]
    Number_of_genes = f3.shape[1]
    ambientness = f3.sum()
    pd.DataFrame([{'pool':pool,'tranche':tranche,'ambientness':ambientness,'Number_of_genes':Number_of_genes,'Number_of_cells':Number_of_cells}]).to_csv(f'/lustre/scratch123/hgi/projects/cardinal_analysis/qc/{tranche}/Donor_Quantification/{pool}/ambientness_{pool}.tsv',sep='\t',index=False)
    all_ambientness.append({'pool':pool,'tranche':tranche,'ambientness':ambientness,'Number_of_genes':Number_of_genes,'Number_of_cells':Number_of_cells})
    del adata_cellbender
    del filtered_adata_cellbender_un
    del adata_cellbender_un

pd.DataFrame(all_ambientness).to_csv('/lustre/scratch123/hgi/projects/cardinal_analysis/qc/ambientness.tsv',sep='\t',index=False)
# adata_cellranger_raw = sc.read_10x_mtx('/lustre/scratch125/humgen/teams/hgi/mo11/oneK1k/extra0_cellspPanel_subsampling/results_extra_0/nf-preprocessing/cellbender/pool3/cellbender-epochs_250__learnrt_0pt000005__zdim_100__zlayer_500__lowcount_10/cellbenderFPR_0pt1filtered_10x_mtx')
# adata_cellranger_filtered = scanpy.read_10x_mtx(f"{df_raw.loc[expid, 'data_path_10x_format']}/filtered_feature_bc_matrix")
# ad_lane_filtered = scanpy.read_10x_mtx(f"{df_raw.loc[expid, 'data_path_10x_format']}/filtered_feature_bc_matrix")