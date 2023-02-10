import pandas as pd
# bsub -Is -G hgi -R'select[mem>90000] rusage[mem=90000]' -M 90000 -q normal -J mo11_workspace /bin/bash
# python -m debugpy --listen 0.0.0.0:5678 --wait-for-client compare_sites.py


# Cellsnp_Sites = pd.read_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/analysis/mo11/cellsnp_sites_file_expanded/cellsnp_sites.tsv')
# UKBB_Sites = pd.read_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/analysis/mo11/cellsnp_sites_file_expanded/ukbb_all_sites.tsv')
# Currently_Utilised = pd.read_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/analysis/mo11/cellsnp_sites_file_expanded/data_ukbb_elgh_cellsnp.tsv')
# ELGH_Sites = pd.read_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/analysis/mo11/cellsnp_sites_file_expanded/data_ukbb_elgh_cellsnp.tsv')
ELGH_SITES_BED = pd.read_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/analysis/mo11/cellsnp_sites_file_expanded/full_elgh_not_merged_sites2.tsv',index_col=0)
ELGH_SITES_BED_head = ELGH_SITES_BED.head()
ELGH_SITES_BED.identifier = ELGH_SITES_BED.identifier.str.replace('chr','')
ELGH_SITES_BED['#CHROM']=ELGH_SITES_BED['#CHROM'].str.replace('chr','')
UKBB_SITES_BED = pd.read_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/analysis/mo11/cellsnp_sites_file_expanded/full_ukbb_all_sites.tsv',index_col=0)

UKBB_SITES_BED.identifier = UKBB_SITES_BED.identifier.str.replace('chr','')
UKBB_SITES_BED_head = UKBB_SITES_BED.head()
# UKBB_SITES_BED['#CHROM']=UKBB_SITES_BED['#CHROM'].str.replace('chr','')
# UKBB_SITES_BED_test = pd.concat([UKBB_SITES_BED_head,ELGH_SITES_BED_head])
UKBB_SITES_BED = pd.concat([UKBB_SITES_BED,ELGH_SITES_BED])
UKBB_SITES_BED = UKBB_SITES_BED.drop_duplicates(subset=['identifier'])
UKBB_SITES_BED = UKBB_SITES_BED.drop(['identifier'], axis=1)
UKBB_SITES_BED.to_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/analysis/mo11/files/all_ukbb_elgh_sites.csv',sep='\t',index=False)
print('done')

del ELGH_SITES_BED
UKBB_SITES_BED.identifier = UKBB_SITES_BED.identifier.str.replace('chr','')
UKBB_SITES_BED['#CHROM']=UKBB_SITES_BED['#CHROM'].str.replace('chr','')
UKBB_SITES_BED = UKBB_SITES_BED.drop_duplicates(subset=['identifier'])
UKBB_SITES_BED.to_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/analysis/mo11/files/all_ukbb_elgh_sites.csv',sep='\t',index=False)
elgh_sites = set(ELGH_SITES_BED.identifier)
ukbb_sites = set(UKBB_SITES_BED.identifier)
uniq_elgh = elgh_sites - ukbb_sites
uniq_ukb =  ukbb_sites - elgh_sites
ELGH_SITES_BED = ELGH_SITES_BED.set_index('identifier')
ELGH_SITES_BED=ELGH_SITES_BED.loc[uniq_elgh]
len(uniq_elgh)
len(uniq_ukb)

ukb_set = set(UKBB_Sites['0'])
elgh_set = set(ELGH_Sites['0'])
current_set_in_genotypes = set(Currently_Utilised['0'])
cellsnp = set(Cellsnp_Sites['0'])
overlap_ukbb = ukb_set.intersection(elgh_set)
uniqu_elgh = elgh_set.difference(cellsnp)
uniqu_ukbb = ukb_set.difference(cellsnp)
len(uniqu_ukbb)
print('Done')