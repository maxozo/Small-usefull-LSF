import pandas as pd
import glob
import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# Are the deconvoluted cells before the same as deconvoluted cells now?
# D_before = pd.read_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc_with_GT/UKBB_ELGH_5th_July_2022/results_rsync2/results/concordances/CRD_CMB12979968/CRD_CMB12979968__joined_df_for_plots.tsv',sep='\t')
# All_assignemsts_before = pd.read_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc_with_GT/UKBB_ELGH_5th_July_2022/results_rsync2/results/deconvolution/vireo/CRD_CMB12979968/vireo_CRD_CMB12979968/donor_ids.tsv',sep='\t')
# All_assignemsts_before = All_assignemsts_before.set_index('cell')
# D_now = pd.read_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc_with_GT/UKBB_ELGH_5th_July_2022/results_with_GT__v1/concordances/CRD_CMB12979968/CRD_CMB12979968__joined_df_for_plots.tsv',sep='\t')
# All_assignemsts_now = pd.read_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc_with_GT/UKBB_ELGH_5th_July_2022/results_with_GT__v1/deconvolution/vireo/CRD_CMB12979968/vireo_CRD_CMB12979968/donor_ids.tsv',sep='\t')
# All_assignemsts_now = All_assignemsts_now.set_index('cell')

# D_before = D_before.set_index('index')
# D_now = D_now.set_index('index')
# D_before['Unnamed: 0_2']=D_now['Unnamed: 0']

# D_before2 = D_before[D_before['Unnamed: 0_2']==D_before['Unnamed: 0_2']]
# set(D_before.index)-set(D_before.index)

# cells_before_assigned_differently_thennow = D_before2[D_before2['Unnamed: 0']!=D_before2['Unnamed: 0_2']]
# cells_now_assigned_differently_before = D_before2[D_before2['Unnamed: 0_2']!=D_before2['Unnamed: 0']]
# cells_assigned_now_but_missing_before = set(D_now.index)-set(D_before.index)
# cells_missing_now_but_assigned_before = set(D_before.index)-set(D_now.index)

# # Now investigate what has happened with these missing cells.
# set(All_assignemsts_before.loc[cells_assigned_now_but_missing_before]['donor_id'])



# import collections
# counter = collections.Counter(All_assignemsts_now.loc[cells_missing_now_but_assigned_before]['donor_id'])
# Swap_Distribution = pd.DataFrame.from_dict(counter, orient='index').reset_index()

# # cells before that are not assigned now:

# Data_to_investigate_best_concordances = pd.read_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc_with_GT/Cardinal_45222_Jul_18_2022/results_with_GT__v1_bcftools118_AGremove/concordances/CRD_CMB12968552/discordant_sites_in_other_donors.tsv',sep='\t')
# Not_Correctly_assigned = Data_to_investigate_best_concordances[Data_to_investigate_best_concordances['same_as_asigned_donor']==False]
# Donor_Saps = pd.read_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc_with_GT/Cardinal_45222_Jul_18_2022/results_with_GT__v1_bcftools118_AGremove/concordances/CRD_CMB12968552/CRD_CMB12968552__joined_df_for_plots.tsv',sep='\t')
# Donor_Saps = Donor_Saps.set_index('index')
# Not_Correctly_assigned = Data_to_investigate_best_concordances.set_index('GT 1')
# Donor_Saps['same_as_asigned_donor']=Not_Correctly_assigned['same_as_asigned_donor']

# Subsampling_itterations = Donor_Saps[Donor_Saps['Nr times becoming different donor in subsampling']!=0]
# Subsampling_itterations['same_as_asigned_donor']==False

# # we plot the info of whether the cellls that swap identities are the same as the ones that has a better donor in terms of concordances

# Donor_Saps['Nr_strict_discordant']/Donor_Saps['Total_sites']*100
# Donor_Saps['Percent_strict_discordant']

# fig, ax = plt.subplots(figsize=(6, 6))
# sns.scatterplot(
#     data=Donor_Saps,
#     x="Percent_strict_discordant",
#     y="Total_reads",
#     color="k",label=f"total nr cells assigned to donor={len(Donor_Saps)}",
#     ax=ax, alpha=0.5
# )
# Donor_Saps_sub = Donor_Saps[Donor_Saps['same_as_asigned_donor']==False]
# sns.scatterplot(
#     data=Donor_Saps_sub,
#     x="Percent_strict_discordant",
#     y="Total_reads",
#     color="r", label=f"becoming different donor; total={len(Donor_Saps_sub)}",
#     ax=ax,
# )
# ax.legend()
# fig.savefig('sites_vs_concordance_t3.png')
# fig.clf()




# all_tranche_files = glob.glob('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc_with_GT/*/results_with_GT__v1/concordances/all_variants_description.tsv')
# Combined_reports = pd.DataFrame()
# for file2 in all_tranche_files:
#     file2
#     file_r = pd.read_csv(file2,sep='\t')
#     Combined_reports = pd.concat([Combined_reports,file_r])

# Need to add stats on how many UKB, ELGH and THP1 are in these pools.
def combine(path_pattern,include_patterns=None):
    all_tranche_files = glob.glob(path_pattern)
    if include_patterns:
        all_tranches = []
        for s in include_patterns:
            for tr1 in all_tranche_files:
                if s in tr1:
                   all_tranches.append(tr1) 
    else:
        all_tranches=all_tranche_files
    Combined_reports = pd.DataFrame()
    for file2 in all_tranches:
        file2
        file_r = pd.read_csv(file2,sep='\t')
        Combined_reports = pd.concat([Combined_reports,file_r])
    print('Done')
    return Combined_reports
    
  
def combine_with_pool(path_pattern):
    all_tranche_files = glob.glob(path_pattern)
    Combined_reports = pd.DataFrame()
    for file2 in all_tranche_files:
        file2
        pool=file2.split('/')[-2]
        file_r = pd.read_csv(file2,sep='\t')
        file_r['pool']=pool
        Combined_reports = pd.concat([Combined_reports,file_r])
    print('Done')
    return Combined_reports    
  
    
#################
################ Check for donors analysed now that were not there before.
# Load all the previous assignments ,include_patterns=['Cardinal_45222_Jul_18_2022','Cardinal_45538_Aug_11_2022','Cardinal_46019_Oct_20_2022','Cardinal_46499_Jan_21_2023','Cardinal_47469_Jun_16_2023','ELGH_9th_May_2022','UKBB_ELGH_5th_July_2022','ELGH_26thMay_2022']
previous_assignments = combine('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc/*/results_rsync2/results/deconvolution/vireo_gt_fix/assignments_all_pools.tsv',include_patterns=['Cardinal_45222_Jul_18_2022','Cardinal_45538_Aug_11_2022','Cardinal_46019_Oct_20_2022','Cardinal_46499_Jan_21_2023','Cardinal_47469_Jun_16_2023','ELGH_9th_May_2022','UKBB_ELGH_5th_July_2022','ELGH_26thMay_2022'])
previous_assignments =previous_assignments[previous_assignments['tranche'].isin(['Cardinal_45222_Jul_18_2022','Cardinal_45538_Aug_11_2022','Cardinal_46019_Oct_20_2022','Cardinal_46499_Jan_21_2023','Cardinal_47469_Jun_16_2023','ELGH_9th_May_2022','UKBB_ELGH_5th_July_2022','ELGH_26thMay_2022'])]
previous_assignments = previous_assignments[previous_assignments['Match Expected']==True]
donors_identified_init = set(previous_assignments['donor_gt'])
len(donors_identified_init)
# Load the current assignments
current_assignments = combine('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc_with_GT/*/results_with_GT__v1/deconvolution/vireo_gt_fix/assignments_all_pools.tsv')
current_assignments.to_csv('/lustre/scratch123/hgi/projects/cardinal_analysis/freezes/freeze2/all___assignments_all_pools.tsv',sep='\t',index=False)

current_assignments = pd.read_csv('/lustre/scratch123/hgi/projects/cardinal_analysis/freezes/freeze2/all___assignments_all_pools.tsv',sep='\t')
expected = current_assignments[current_assignments['Match Expected']]
expected['experiment_id'] = expected['pool']+'__'+expected['donor_gt'].str.replace('^0*', '').str.replace('\.0*', '')
expected = expected.set_index('experiment_id')
expected['State'] = State_metadata['State']

# Now we add stats about the pass fail rate
all_donor_data = combine('/lustre/scratch123/hgi/projects/cardinal_analysis/freezes/freeze2/*/Summary_plots/Summary/*_Donor_Report.tsv')
all_donor_data2 = combine('/lustre/scratch123/hgi/projects/cardinal_analysis/freezes/freeze2/*/Summary_plots/Summary/UKBB_REPORT/*_UKBB_Report.tsv')
all_donor_data3 = combine('/lustre/scratch123/hgi/projects/cardinal_analysis/freezes/freeze2/*/Summary_plots/Summary/ELGH_REPORT/*_ELGH_Report.tsv')
all_donor_data4 = pd.concat([all_donor_data,all_donor_data2,all_donor_data3])
all_donor_data4
all_donor_data4['experiment_id'] = all_donor_data4['Pool ID']+'__'+all_donor_data4['Vacutainer ID'].str.replace('^0*', '').str.replace('\.0*', '')
all_donor_data = all_donor_data4.drop_duplicates('experiment_id')
all_exp = pd.DataFrame(set(expected.index) - set(all_donor_data['experiment_id']))
all_exp2 = set(all_donor_data['experiment_id']) - set(expected.index)

missing_from_final_reports  = set(all_exp[~all_exp[0].str.contains('celline')][0])
expected.loc[missing_from_final_reports].iloc[0]
# We want to extrsact all missing now
all_missing = current_assignments[~current_assignments['Missing'].isna()]
all_missing['explode_col2'] = all_missing['Missing']
all_missing['explode_col'] = all_missing['Missing'].astype(str).str.split(';')
all_missing = all_missing.explode('explode_col')
all_missing['explode_col'] = all_missing['explode_col'].astype(str)
all_missing['explode_col'] = all_missing['explode_col'].astype(str).str.replace('^0*', '')
all_missing['explode_col'] = all_missing['explode_col'].str.replace('\.0*', '')
all_missing['experiment_id'] = all_missing['pool']+'__'+all_missing['explode_col']
all_missing = all_missing.drop_duplicates('experiment_id')
all_missing = all_missing.set_index('experiment_id')
all_missing['State']= State_metadata['State']

# There are samples where there is no sample metadata in any datasheets.


State_metadata = pd.read_csv('/lustre/scratch123/hgi/projects/cardinal_analysis/freezes/combined_metadata_v2.tsv',sep='\t')
State_metadata['experiment_id'] = State_metadata['experiment_id'].str.split('__').str[0] + '__' + State_metadata['experiment_id'].str.split('__').str[1].astype(str).str.replace('^0*', '').str.replace('\.0*', '')
State_metadata = State_metadata.set_index('experiment_id')
Metadata['donor'].astype(str).str.replace('^0*', '')

set(State_metadata['State'])


current_assignments = current_assignments[current_assignments['tranche'].isin(['Cardinal_45222_Jul_18_2022','Cardinal_45538_Aug_11_2022','Cardinal_46019_Oct_20_2022','Cardinal_46499_Jan_21_2023','Cardinal_47469_Jun_16_2023','ELGH_9th_May_2022','UKBB_ELGH_5th_July_2022','ELGH_26thMay_2022',])]
current_assignments = current_assignments[current_assignments['Match Expected']==True]
donors_identified_now = set(current_assignments['donor_gt'])
len(donors_identified_now)

missing_donors_identified_before = donors_identified_init - donors_identified_now
missing_donors_identified_before_df = previous_assignments[previous_assignments['donor_gt'].isin(missing_donors_identified_before)]
m2 = missing_donors_identified_before_df[['donor_gt','tranche','pool','donor_gt original']]
m2 = m2[m2.donor_gt != 'THP1']
m2 = m2[m2.donor_gt != 'U937']
m2.to_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/tmp/to_investigate.tsv',sep='\t')

# investigate = pd.read_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc/Cardinal_45222_Jul_18_2022/results_rsync2/results/gtmatch/CRD_CMB12968557/pool_CRD_CMB12968557_panel_GT_ELGH_gtcheck_score_table.csv')
# comb=pd.DataFrame()
# for id1 in set(investigate.index):
#     print(id1)
#     m2 = investigate.loc[id1].sort_values(by=['gtcheck_score'],ascending=False)[:4]
#     comb=pd.concat([comb,m2])
# comb.to_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/tmp/investigate2.tsv',sep='\t')
# Check for newly identified IDs
#          donor_gt                     tranche             pool
# 84    30007475525  Cardinal_45222_Jul_18_2022  CRD_CMB12968561
# 100  S2-046-00823  Cardinal_45222_Jul_18_2022  CRD_CMB12968557
# 81   S2-999-90220  Cardinal_45538_Aug_11_2022  CRD_CMB13076385
# 95   S2-046-00720  Cardinal_45538_Aug_11_2022  CRD_CMB13076381
# 72   S2-046-00942  Cardinal_46019_Oct_20_2022  CRD_CMB13195930
# 77   S2-999-90371  Cardinal_46019_Oct_20_2022  CRD_CMB13195930
# 115  S2-046-00626  Cardinal_46019_Oct_20_2022  CRD_CMB13195927
# 70   S2-046-00622     UKBB_ELGH_5th_July_2022  CRD_CMB12979965

#################
#################



combined_metadata = combine('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/fetch/*/results/yascp_inputs/Extra_Metadata.tsv')
combined_metadata=combined_metadata.set_index('experiment_id')
combined_ambientness = combine('/lustre/scratch123/hgi/projects/cardinal_analysis/qc/*/Donor_Quantification/*/ambientness_[!per]*.tsv')
combined_ambientness=combined_ambientness.set_index('pool')
combined = combined_metadata.join(combined_ambientness)

pass_fail_ukb_tresholds = combine('/lustre/scratch123/hgi/projects/cardinal_analysis/qc/*/Summary_plots/Summary/*_Tranche_Report.tsv')
pass_fail_ukb_tresholds=pass_fail_ukb_tresholds.set_index('Pool id')
combined = combined.join(pass_fail_ukb_tresholds)

combined_PASS = combined[combined['Tranche Pass/Fail']=='PASS']
combined_PASS['ambientness_per_cell']= combined_PASS['ambientness']/combined_PASS['Number_of_cells']
combined_PASS['cohort'] = ''

UKB_ONLY_POOLS = combined_PASS[(combined_PASS['nr_elgh_samples']==0) & (combined_PASS['nr_ukbb_samples']>0)]
combined_PASS.loc[(combined_PASS['nr_elgh_samples']==0) & (combined_PASS['nr_ukbb_samples']>0),'cohort']='UKB_ONLY'
ELGH_ONLY_POOLS = combined_PASS[(combined_PASS['nr_elgh_samples']>0) & (combined_PASS['nr_ukbb_samples']==0)]
combined_PASS.loc[(combined_PASS['nr_elgh_samples']>0) & (combined_PASS['nr_ukbb_samples']==0),'cohort']='ELGH_ONLY'
MIXED_POOLS = combined_PASS[(combined_PASS['nr_elgh_samples']>0) & (combined_PASS['nr_ukbb_samples']>0)]
combined_PASS.loc[(combined_PASS['nr_elgh_samples']>0) & (combined_PASS['nr_ukbb_samples']>0),'cohort']='MIXED'
combined_PASS = combined_PASS[combined_PASS['cohort'] != '']


# #############
############### INITIAL APPROACH
############ PLOT TO SHOW THE AMBIENTNESS DISTRIBUTIONS AND THE POOLS WE ARE PICKING
import seaborn as sns
fig, (ax1) = plt.subplots(1, 1,figsize=(13, 6))
sns.distplot(UKB_ONLY_POOLS['ambientness_per_cell'],ax=ax1,color='b',label='UKB_ONLY')
sns.distplot(ELGH_ONLY_POOLS['ambientness_per_cell'],ax=ax1,color='r',label='ELGH_ONLY')
sns.distplot(MIXED_POOLS['ambientness_per_cell'],ax=ax1,color='g',label='MIXED_POOLS')
# add lines for the pools that we are looking att
for val in MIXED_POOLS[MIXED_POOLS['Experiment id']=='Cardinal_46499_Jan_21_2023']['ambientness_per_cell']:
    print(val)
    plt.axvline(x=val,color='g') 

for val in ELGH_ONLY_POOLS[ELGH_ONLY_POOLS['Experiment id']=='Cardinal_46499_Jan_21_2023']['ambientness_per_cell']:
    print(val)
    plt.axvline(x=val,color='r') 

for val in UKB_ONLY_POOLS[UKB_ONLY_POOLS['Experiment id']=='Cardinal_46499_Jan_21_2023']['ambientness_per_cell']:
    print(val)
    plt.axvline(x=val,color='b') 

ax1.legend()
fig.savefig('ambientness_ppl.png')
fig.clf()

##############
##############
##############


# #############
############### SECOND APPROACH
############ PLOT TO SHOW THE AMBIENTNESS DISTRIBUTIONS AND THE POOLS WE ARE PICKING
import seaborn as sns
fig, (ax1) = plt.subplots(1, 1,figsize=(13, 6))
scatter_plot = sns.displot(data=combined_PASS, x="ambientness_per_cell", hue='cohort', multiple="dodge",kde=True, binwidth=20, height=8.27, aspect=11.7/8.27, shrink=1.)

for tr1 in ['Cardinal_45222_Jul_18_2022','Cardinal_45538_Aug_11_2022','Cardinal_46019_Oct_20_2022','Cardinal_46499_Jan_21_2023','Cardinal_47469_Jun_16_2023','ELGH_9th_May_2022','UKBB_ELGH_5th_July_2022','ELGH_26thMay_2022']:
    for val in MIXED_POOLS[MIXED_POOLS['Experiment id']==tr1]['ambientness_per_cell']:
        print(val)
        plt.axvline(x=val,color='g',alpha=.2,linestyle ='--') 

    for val in ELGH_ONLY_POOLS[ELGH_ONLY_POOLS['Experiment id']==tr1]['ambientness_per_cell']:
        print(val)
        plt.axvline(x=val,color='b',alpha=.2,linestyle ='--') 

    for val in UKB_ONLY_POOLS[UKB_ONLY_POOLS['Experiment id']==tr1]['ambientness_per_cell']:
        print(val)
        plt.axvline(x=val,color='orange',alpha=.2,linestyle ='--') 
    
scatter_plot.fig.savefig("ambientness_ppl.png")
fig.clf()

##############
##############
##############


# #############
############### 
############ FINDING POOLS THAT CONTAIN ALL COMBINATIONSTÊÊÊ

UKB_ONLY_POOLS = UKB_ONLY_POOLS[(UKB_ONLY_POOLS['ambientness_per_cell']>50) & (UKB_ONLY_POOLS['ambientness_per_cell']<100)]
ELGH_ONLY_POOLS = ELGH_ONLY_POOLS[(ELGH_ONLY_POOLS['ambientness_per_cell']>50) & (ELGH_ONLY_POOLS['ambientness_per_cell']<100)]
MIXED_POOLS = MIXED_POOLS[(MIXED_POOLS['ambientness_per_cell']>50) & (MIXED_POOLS['ambientness_per_cell']<100)]
set(MIXED_POOLS.index)
set(UKB_ONLY_POOLS['Experiment id']).intersection(ELGH_ONLY_POOLS['Experiment id'])



############### CELL LEVEL ANALYSIS
################################
Combined_reports = pass_fail_ukb_tresholds
combined = combine('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc_with_GT/*/results_with_GT__v1/concordances/joined_df_for_plots.tsv',include_patterns=['Cardinal_45222_Jul_18_2022','Cardinal_45538_Aug_11_2022','Cardinal_46019_Oct_20_2022','Cardinal_46499_Jan_21_2023','Cardinal_47469_Jun_16_2023','ELGH_9th_May_2022','UKBB_ELGH_5th_July_2022','ELGH_26thMay_2022'])
combined_sites_info = combine('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc_with_GT/*/results_with_GT__v1/concordances/all_variants_description.tsv')
combined['Tranche Pass/Fail']=''
combined['informative positions cellsp called on']=0
combined['uninformative positions cellsp called on']=0
combined['total number of positions cellsp called on']=0
Combined_reports = Combined_reports.reset_index()
combined = combined.reset_index()
##################
################# ADDING NUMBER OF INFORMATIVE SITES CALLED ON
for id1 in set(combined['pool id']):
    print(id1)
    try:
        combined.loc[combined['pool id']==id1,'Tranche Pass/Fail']=Combined_reports[Combined_reports['Pool id']==id1]['Tranche Pass/Fail'].values[0]
        combined.loc[combined['pool id']==id1,'informative positions cellsp called on']=combined_sites_info[combined_sites_info['sample']==id1]['informative positions cellsp called on'].values[0]
        combined.loc[combined['pool id']==id1,'uninformative positions cellsp called on']=combined_sites_info[combined_sites_info['sample']==id1]['uninformative positions cellsp called on'].values[0]
        combined.loc[combined['pool id']==id1,'total number of positions cellsp called on']=combined_sites_info[combined_sites_info['sample']==id1]['total number of positions cellsp called on'].values[0]
    except:
        _='still finishing'  
############
##############   ADDING NUMBER OF CELLS DONOR HAS AS WE WANT TO FILTER DOWN TO >200 CELLS PER DONOR
combined['nr_cell_per_donor'] = 0
combined['Donor_Pool']= combined['donor_id']+':'+combined['pool id']
for pool_donor in set(combined['Donor_Pool']):
    combined.loc[combined['Donor_Pool']==pool_donor,'nr_cell_per_donor'] = len(combined[combined['Donor_Pool']==pool_donor])

###################
###################

combined_discordances = combine_with_pool('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc_with_GT/*/results_with_GT__v1/concordances/*/discordant_sites_in_other_donors.tsv')
path_pattern='/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc_with_GT/*/results_with_GT__v1/concordances/*/discordant_sites_in_other_donors.tsv'
combined_discordances_com =combined_discordances.set_index(combined_discordances['pool']+'---'+combined_discordances['GT 1'])
combined = combined.set_index(combined['pool id']+'---'+combined['index'])
combined['same_as_asigned_donor']=combined_discordances_com['same_as_asigned_donor']

Currently_analysed = combined_discordances_com[~combined_discordances_com['Total_sites_other_donor'].isna()]
fa = Currently_analysed[Currently_analysed['same_as_asigned_donor']==False]
Currently_analysed[~Currently_analysed['GT 2'].isin(Currently_analysed['Donor_With_Highest_Concordance'].values.tolist())]

for i,row1 in Currently_analysed.iterrows():
    print(i)

combined_discordances_com_False = combined_discordances_com[combined_discordances_com['same_as_asigned_donor']==False]
combined_discordances_com_False = combined_discordances_com_False[combined_discordances_com_False['Lowest_Disconcordance_value_in_all_donors']!=combined_discordances_com_False['Percent_Discordant']]
combined_discordances_com_False.iloc[0]
# # ##### HUE PLOTS

# fig, ax = plt.subplots(figsize=(6, 6))
# sns.scatterplot(
#     data=Joined_Df,
#     y="nr_cell_per_donor",hue='nr_cell_per_donor',
#     x="cell ambientness",label=f"total nr cells assigned to donor={len(Joined_Df)}",
#     ax=ax, alpha=0.5
# )

# fig.savefig('nr_cells_ambientness_vs_concordance.png')
# fig.clf()

#######
####### LIMIT TO CELLS THAT PASS FILTERS
Data_used_before = pd.read_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/metadata/to_use_for_calculations_noSwaps.tsv',sep='\t')
all_ids_before = set(Data_used_before['pool id'])
all_ids_now = set(combined['pool id'])
all_ids_before-all_ids_now
Joined_Df= combined
Joined_Df=Joined_Df[Joined_Df['nr_cell_per_donor']>=200]
Joined_Df = Joined_Df[Joined_Df['pool id']!='CRD_CMB12979968']
# Joined_Df = Joined_Df[Joined_Df['pool id'] != 'CRD_CMB12968552']
Joined_Df['total number of sites']=Joined_Df['Nr_Concordant']+Joined_Df['Nr_Discordant']
Joined_Df = Joined_Df[Joined_Df['Tranche Pass/Fail']!='FAIL']
# Joined_Df=Joined_Df[Joined_Df['cell ambientness']<10000]
# Joined_Df=Joined_Df[Joined_Df['Discordant_reads']<1000]
# After filtering we now plot the distributions of data that we are analysing.
#############
#############
Joined_Df = Joined_Df.set_index('index')
# HERE - do plots
background_cell_swaps = Joined_Df[Joined_Df['Nr times becoming different donor in subsampling']!=0]
background_NoSwaps = Joined_Df[Joined_Df['Nr times becoming different donor in subsampling']==0]


MAD = Joined_Df['prob_max'].mad()
median =  Joined_Df['prob_max'].median()
MAD_2 = median-3*MAD
mad_probmax=MAD_2
prob_max_filter_swap = background_cell_swaps[background_cell_swaps['prob_max']>=MAD_2]
prob_max_filter_Noswap = background_NoSwaps[background_NoSwaps['prob_max']>=MAD_2]
(len(background_NoSwaps)-len(prob_max_filter_Noswap))/len(background_NoSwaps)*100
(len(background_cell_swaps)-len(prob_max_filter_swap))/len(background_cell_swaps)*100

MAD = Joined_Df['Percent_strict_discordant'].mad()
median =  Joined_Df['Percent_strict_discordant'].median()
MAD_2 = median+3*MAD
mad_disc=MAD_2
prob_max_filter_swap = background_cell_swaps[background_cell_swaps['Percent_strict_discordant']<MAD_2]
prob_max_filter_Noswap = background_NoSwaps[background_NoSwaps['Percent_strict_discordant']<MAD_2]
(len(background_NoSwaps)-len(prob_max_filter_Noswap))/len(background_NoSwaps)*100
(len(background_cell_swaps)-len(prob_max_filter_swap))/len(background_cell_swaps)*100
prob_max_filter_swap_removed = background_cell_swaps[background_cell_swaps['Percent_strict_discordant']>=MAD_2]
set(prob_max_filter_swap_removed['Unnamed: 0'])

MAD = Joined_Df['Discordant_reads_by_n_sites'].mad()
median =  Joined_Df['Discordant_reads_by_n_sites'].median()
MAD_2 = median+3*MAD
mad_mm = MAD_2
MM_filter_swap = background_cell_swaps[background_cell_swaps['Discordant_reads_by_n_sites']<MAD_2]
MM_filter_Noswap = background_NoSwaps[background_NoSwaps['Discordant_reads_by_n_sites']<MAD_2]
(len(background_NoSwaps)-len(MM_filter_Noswap))/len(background_NoSwaps)*100
(len(background_cell_swaps)-len(MM_filter_swap))/len(background_cell_swaps)*100
MM_filter_swap_removed = background_cell_swaps[background_cell_swaps['Discordant_reads_by_n_sites']>=MAD_2]
set(prob_max_filter_swap_removed['Unnamed: 0'])-set(MM_filter_swap_removed['Unnamed: 0'])
set(MM_filter_swap_removed['Unnamed: 0'])-set(prob_max_filter_swap_removed['Unnamed: 0'])

strict_discordant_filter = Joined_Df[Joined_Df['Percent_strict_discordant']<10]
remaining_flips =strict_discordant_filter[strict_discordant_filter['Nr times becoming different donor in subsampling']!=0]
(len(Joined_Df)-len(strict_discordant_filter))/len(Joined_Df)*100

MAD_Keep = Joined_Df
# MAD_Keep=MAD_Keep[MAD_Keep['prob_max']>=mad_probmax]
MAD_Keep=MAD_Keep[MAD_Keep['Percent_strict_discordant']<mad_disc]
MAD_Keep=MAD_Keep[MAD_Keep['Discordant_reads_by_n_sites']<mad_mm]

new_cell_swaps = MAD_Keep[MAD_Keep['Nr times becoming different donor in subsampling']!=0]
new_NoSwaps = MAD_Keep[MAD_Keep['Nr times becoming different donor in subsampling']==0]
(len(background_NoSwaps)-len(new_NoSwaps))/len(background_NoSwaps)*100
(len(background_cell_swaps)-len(new_cell_swaps))/len(background_cell_swaps)*100


MAD_Keep = Joined_Df
MAD_Keep1=MAD_Keep[MAD_Keep['prob_max']<mad_probmax]
MAD_Keep2=MAD_Keep[MAD_Keep['Percent_strict_discordant']>=mad_disc]
MAD_Keep3=MAD_Keep[MAD_Keep['Discordant_reads_by_n_sites']>=mad_mm]

len(set(MAD_Keep1['Unnamed: 0']+MAD_Keep1['pool id']))
set1 = set(MAD_Keep1['Unnamed: 0']+MAD_Keep1['pool id'])
set2 = set(MAD_Keep2['Unnamed: 0']+MAD_Keep1['pool id'])
set3 = set(MAD_Keep3['Unnamed: 0']+MAD_Keep1['pool id'])

import matplotlib.pyplot as plt
from matplotlib_venn import venn3 
from matplotlib_venn import venn2
def Venn2(set1,set2):
    A = len(set1-set2)
    B = len(set1.intersection(set2))
    C = len(set2-set1)
    fig, ax = plt.subplots(figsize=(6, 6))
    venn2(subsets = (A, C, B), set_labels = ('Group A', 'Group B'),ax=ax)
    ax.legend()
    fig.savefig('Venn______15_08_2023.png')
    fig.clf()

def Venn3(set1,set2,set3):
    
    A_set1 = set1-set3
    B_set2 = set2-set3
    A = len(A_set1-B_set2)
    B = len(A_set1.intersection(B_set2))
    C = len(B_set2-A_set1)
    
    B_set2 = set2-set1
    C_set2 = set3-set1
    A_2 = len(B_set2-C_set2)
    B_2 = len(B_set2.intersection(C_set2))
    C_2 = len(C_set2-B_set2)    
    
    A_set3 = set1-set2
    C_set3 = set3-set2
    A_3 = len(A_set3-C_set3)
    B_3 = len(A_set3.intersection(C_set3))
    C_3 = len(C_set3-A_set3)       
    
    intersect1 = len(set1.intersection(set2))

    fig, ax = plt.subplots(figsize=(6, 6))
    venn3(subsets = (A, C, B, C_3,B_3,B_2,intersect1),ax=ax)
    ax.legend()
    fig.savefig('Venn______15_08_2023.png')
    fig.clf()


# MAD_Keep = MAD_Keep[MAD_Keep['Discordant_reads_by_n_sites']<0.10]
fig, ax = plt.subplots(figsize=(6, 6))
sns.scatterplot(
    data=MAD_Keep,
    x="Percent_strict_discordant",
    y="total number of sites",
    color="k",label=f"total nr cells assigned to donor={len(MAD_Keep)}",
    ax=ax, alpha=0.5
)
MAD_Keep_sub = MAD_Keep[MAD_Keep['Nr times becoming different donor in subsampling']!=0]

sns.scatterplot(
    data=MAD_Keep_sub,
    x="Percent_strict_discordant",
    y="total number of sites",
    color="r", label=f"becoming different donor; total={len(MAD_Keep_sub)}",
    ax=ax,
)
try:
    sns.kdeplot(
        data=MAD_Keep_sub,
        x="Percent_strict_discordant",
        y="total number of sites",
        color='r',
        fill=True,
        alpha=0.6,
        cut=2,
        ax=ax,
    )
except:
    _='only two entris, so cant do a density'
ax.legend()
fig.savefig('TotalAnalysis__strictDiscordant_reads_by_n_sites______15_08_2023.png')
fig.clf()


# violin_of_swaps
ax1 = sns.violinplot(data=MAD_Keep,y="total number of sites", x="Nr times becoming different donor in subsampling", cut=0, scale='width')
fig = ax1.get_figure()
fig.savefig('TotalAnalysis_Discordant_reads_by_n_sites_different_donor22.png')
fig.clf()

# MAD calculations
MAD = Joined_Df['prob_max'].mad()
median =  Joined_Df['prob_max'].median()
MAD_5 = median-10*MAD
Joined_Df[Joined_Df['prob_max']<MAD_5]

MAD = Joined_Df['Percent_strict_discordant'].mad()
median =  Joined_Df['Percent_strict_discordant'].median()
MAD_5 = median+3*MAD
MAD_Excluded = Joined_Df[Joined_Df['Percent_strict_discordant']>MAD_5]
MAD_Excluded_swap = MAD_Excluded[MAD_Excluded['Nr times becoming different donor in subsampling']!=0]
MAD_Keep =  Joined_Df[Joined_Df['Percent_strict_discordant']<=MAD_5]
MAD_Keep = Joined_Df
Joined_Df_swap = Joined_Df[Joined_Df['Nr times becoming different donor in subsampling']!=0]
Donor_swap_ids = Joined_Df_swap[['pool id','donor_id','New Donor Identities','index']]
Donor_swap_ids.to_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/bin/swaps.tsv',sep='\t')

swap_cohorts_cells = ['TTCTAGTAGGGACCAT-1','ACGTACAGTTAGGCCC-1','TCTATACAGCAAACAT-1']

import collections
MAD_Keep_count = MAD_Keep[MAD_Keep['Nr times becoming different donor in subsampling']!=0]
counter = collections.Counter(MAD_Keep_count['pool id'])
Swap_Distribution = pd.DataFrame.from_dict(counter, orient='index').reset_index()



MAD_Keep=Joined_Df
MAD_Keep = MAD_Keep[MAD_Keep['Percent_strict_discordant']<10]

MAD_Keep = MAD_Keep[MAD_Keep['Nr times becoming different donor in subsampling']==0]

MAD_Keep= MAD_Keep[MAD_Keep['Total_sites']>120]

MAD = MAD_Keep['Total_sites'].mad()
median =  Joined_Df['Total_sites'].median()
MAD_5 = median-1*MAD


MAD_Keep =MAD_Keep[MAD_Keep['Discordant_reads_by_n_sites']<.025]
fig, ax = plt.subplots(figsize=(6, 6))
sns.scatterplot(
    data=MAD_Keep,
    x="Percent_strict_discordant",
    y="total number of sites",
    color="k",label=f"total nr cells assigned to donor={len(MAD_Keep)}",
    ax=ax, alpha=0.5
)
# MAD_Keep_sub = MAD_Keep[MAD_Keep['Nr times becoming different donor in subsampling']!=0]
MAD_Keep_sub = MAD_Keep[MAD_Keep['same_as_asigned_donor']!=True]
sns.scatterplot(
    data=MAD_Keep_sub,
    x="Percent_strict_discordant",
    y="total number of sites",
    color="r", label=f"becoming different donor; total={len(MAD_Keep_sub)}",
    ax=ax,
)
try:
    sns.kdeplot(
        data=MAD_Keep_sub,
        x="Percent_strict_discordant",
        y="total number of sites",
        color='r',
        fill=True,
        alpha=0.6,
        cut=2,
        ax=ax,
    )
except:
    _='only two entris, so cant do a density'
ax.legend()
fig.savefig('TotalAnalysis__sites_vs_concordance2333_same_as_assigned.png')
fig.clf()

# Violins
ax1 = sns.violinplot(data=MAD_Keep[MAD_Keep['percent_informative']>0.98], y="percent_informative", x="Nr times becoming different donor in subsampling", cut=0, scale='width')
fig = ax1.get_figure()
fig.savefig('TotalAnalysis_Discordant_reads_by_n_sites_different_donor22.png')
fig.clf()


# MAD_Keep['same_as_asigned_donor']
ax1 = sns.violinplot(data=MAD_Keep, y="total number of sites", x="same_as_asigned_donor", cut=0, scale='width')
fig = ax1.get_figure()
fig.savefig('TotalAnalysis_Discordant_reads_by_n_sites_different_donor_14_08_2023.png')
fig.clf()

# ############ Number of unique donor pairs swapping donors
before_after_donor_ids = MAD_Keep_sub[['donor_id','New Donor Identities','pool id']]
before_after_donor_ids2 = before_after_donor_ids.set_index(before_after_donor_ids.index+'-'+before_after_donor_ids['pool id'] +' '+ MAD_Keep_sub['donor_id'])
before_after_donor_ids_new2 = before_after_donor_ids2['New Donor Identities'].str.split(';').explode()
before_after_donor_ids_new2 = before_after_donor_ids_new2.reset_index()
before_after_donor_ids_new2 = before_after_donor_ids_new2[before_after_donor_ids_new2['New Donor Identities']!='']
expanded = before_after_donor_ids_new2['index'].str.split(' ',expand=True)
expanded['New Donor Identities']=before_after_donor_ids_new2['New Donor Identities']
all_unique_cell_swaps = expanded.drop_duplicates()
all_unique_cell_swaps['Cohor 1']=''
all_unique_cell_swaps['Cohor 2']=''

all_unique_cell_swaps.loc[all_unique_cell_swaps['New Donor Identities'].str.split("_").str[0].str.len()==14,'Cohor 1']='ELGH'
all_unique_cell_swaps.loc[all_unique_cell_swaps['New Donor Identities'].str.split("_").str[0] == all_unique_cell_swaps['New Donor Identities'].str.split("_").str[1],'Cohor 1']='UKB'
all_unique_cell_swaps.loc[all_unique_cell_swaps[1].str.split("_").str[0].str.len()==14,'Cohor 2']='ELGH'
all_unique_cell_swaps.loc[all_unique_cell_swaps[1].str.split("_").str[0] == all_unique_cell_swaps[1].str.split("_").str[1],'Cohor 2']='UKB'

ukb_becoming_elgh = all_unique_cell_swaps[all_unique_cell_swaps['Cohor 1']=='UKB']
ukb_becoming_elgh = ukb_becoming_elgh[all_unique_cell_swaps['Cohor 2']=='ELGH']
elgh_becoming_ukb = all_unique_cell_swaps[all_unique_cell_swaps['Cohor 1']=='ELGH']
elgh_becoming_ukb = elgh_becoming_ukb[all_unique_cell_swaps['Cohor 2']=='UKB']
all_cells_swapping_cohorts = set(elgh_becoming_ukb[0]).union(set(ukb_becoming_elgh[0]))
MAD_Keep_sub = MAD_Keep_sub.set_index(MAD_Keep_sub.index+'-'+MAD_Keep_sub['pool id'])

elgh_becoming_ukb2 = elgh_becoming_ukb.set_index(0)

fig, ax = plt.subplots(figsize=(6, 6))
sns.scatterplot(
    data=MAD_Keep,
    x="Percent_strict_discordant",
    y="total number of sites",
    color="k",label=f"total nr cells assigned to donor={len(MAD_Keep)}",
    ax=ax, alpha=0.5
)
# MAD_Keep_sub2 = MAD_Keep_sub.loc[all_cells_swapping_cohorts]
# MAD_Keep_sub3 =MAD_Keep_sub2[MAD_Keep_sub2['pool id']=='CRD_CMB12979968']
# MAD_Keep_sub2 = 
# elgh_becoming_ukb2.loc[MAD_Keep_sub3.index][[1,'New Donor Identities']]
# t = elgh_becoming_ukb2.loc[MAD_Keep_sub3.index][[1,'New Donor Identities']]
# t.drop_duplicates()
sns.scatterplot(
    data=MAD_Keep_sub2,
    x="Percent_strict_discordant",
    y="total number of sites",
    color="r", label=f"becoming different cohort; total={len(MAD_Keep_sub2)}",
    ax=ax,
)
try:
    sns.kdeplot(
        data=MAD_Keep_sub2,
        x="Percent_strict_discordant",
        y="total number of sites",
        color='r',
        fill=True,
        alpha=0.6,
        cut=2,
        ax=ax,
    )
except:
    _='only two entris, so cant do a density'
ax.legend()
fig.savefig('TotalAnalysis__sites_vs_concordance__becomingDifferentCohort_no9968____4444.png')
fig.clf()




before_after_donor_ids =before_after_donor_ids.set_index('donor_id')
before_after_donor_ids_new = before_after_donor_ids['New Donor Identities'].str.split(';').explode()
before_after_donor_ids_new2 = before_after_donor_ids_new.reset_index()
before_after_donor_ids_new3 = before_after_donor_ids_new2[before_after_donor_ids_new2['New Donor Identities']!='']
before_after_donor_ids_new3= before_after_donor_ids_new3.drop_duplicates()
before_after_donor_ids_new3['combo']= before_after_donor_ids_new3[['donor_id','New Donor Identities']].values.tolist()

# Number of cells changing cohorts.
# UKB donors

# ############### Removing Discordant cells
# HERE
MAD_Keep = combined
MAD_Keep = MAD_Keep[MAD_Keep['Discordant_reads_by_n_sites']<0.10]
fig, ax = plt.subplots(figsize=(6, 6))
sns.scatterplot(
    data=MAD_Keep,
    x="Percent_strict_discordant",
    y="total number of sites",
    color="k",label=f"total nr cells assigned to donor={len(MAD_Keep)}",
    ax=ax, alpha=0.5
)
MAD_Keep_sub = MAD_Keep[MAD_Keep['Nr times becoming different donor in subsampling']!=0]

sns.scatterplot(
    data=MAD_Keep_sub,
    x="Percent_strict_discordant",
    y="total number of sites",
    color="r", label=f"becoming different donor; total={len(MAD_Keep_sub)}",
    ax=ax,
)
try:
    sns.kdeplot(
        data=MAD_Keep_sub,
        x="Percent_strict_discordant",
        y="total number of sites",
        color='r',
        fill=True,
        alpha=0.6,
        cut=2,
        ax=ax,
    )
except:
    _='only two entris, so cant do a density'
ax.legend()
fig.savefig('TotalAnalysis__strictDiscordant_reads_by_n_sites______5555.png')
fig.clf()



all_donor_swaps_happening = set()
for i,row1 in before_after_donor_ids_new3.iterrows():
    print(row1)
    i1 = row1['donor_id']
    i2=row1['New Donor Identities']
    comb=[i1,i2]
    comb.sort()
    mix=';'.join(set(comb))
    all_donor_swaps_happening.add(mix)

all_donor_swaps_happening = pd.DataFrame(all_donor_swaps_happening)
r1 = all_donor_swaps_happening[~all_donor_swaps_happening[0].str.contains('donor')]
r2= r1[~r1[0].str.contains('celline')]
before_after_donor_ids_new3['combo'].values.sort()
before_after_donor_ids_new




# #############
############### SECOND APPROACH AGAIN
############ PLOT TO SHOW THE AMBIENTNESS DISTRIBUTIONS AND THE POOLS WE ARE PICKING
import seaborn as sns
fig, (ax1) = plt.subplots(1, 1,figsize=(13, 6))
scatter_plot = sns.displot(data=combined_PASS, x="ambientness_per_cell", hue='cohort', multiple="dodge",kde=True, binwidth=20, height=8.27, aspect=11.7/8.27, shrink=1.)

for tr1 in ['Cardinal_45222_Jul_18_2022','Cardinal_45538_Aug_11_2022','Cardinal_46019_Oct_20_2022','Cardinal_46499_Jan_21_2023','Cardinal_47469_Jun_16_2023','ELGH_9th_May_2022','UKBB_ELGH_5th_July_2022','ELGH_26thMay_2022']:
    for i,val in MIXED_POOLS[MIXED_POOLS['Experiment id']==tr1].iterrows():
        print(val)
        if i in set(Joined_Df['pool id']):
            plt.axvline(x=val['ambientness_per_cell'],color='g',alpha=.2,linestyle ='--') 

    for i,val in ELGH_ONLY_POOLS[ELGH_ONLY_POOLS['Experiment id']==tr1].iterrows():
        print(val)
        if i in set(Joined_Df['pool id']):
            plt.axvline(x=val['ambientness_per_cell'],color='b',alpha=.2,linestyle ='--') 

    for i,val in UKB_ONLY_POOLS[UKB_ONLY_POOLS['Experiment id']==tr1].iterrows():
        print(val)
        if i in set(Joined_Df['pool id']):
            plt.axvline(x=val['ambientness_per_cell'],color='orange',alpha=.2,linestyle ='--') 
    
scatter_plot.fig.savefig("output.png")
fig.clf()

##############
##############


# ######### PROB_MAX PLOT
##########################
ax1 = sns.violinplot(data=MAD_Keep, y="prob_max", x="Nr times becoming different donor in subsampling", cut=0, scale='width')
fig = ax1.get_figure()
fig.savefig('TotalAnalysis__Removed_becoming_different_donor2.png')
fig.clf()


MAD = MAD_Keep['prob_max'].mad()
median =  MAD_Keep['prob_max'].median()
MAD_3 = median-5*MAD
MAD_Keep_After_Prob_Max = MAD_Keep[MAD_Keep['prob_max'].astype(float)>MAD_3]

########################
########################

# ######### PERCENT STRICT DISCORDANT
##########################
ax1 = sns.violinplot(data=Joined_Df, y="Percent_strict_discordant", x="Nr times becoming different donor in subsampling", cut=0, scale='width')
fig = ax1.get_figure()
fig.savefig('TotalAnalysis__PERCENT_STRICT_DISC_different_donor.png')
fig.clf()

####################
#####################

# ######### Discordant_reads_by_n_sites
##########################

ax1 = sns.violinplot(data=Joined_Df[Joined_Df['Discordant_reads_by_n_sites']<2], y="Discordant_reads_by_n_sites", x="Nr times becoming different donor in subsampling", cut=0, scale='width')
fig = ax1.get_figure()
fig.savefig('TotalAnalysis__Discordant_reads_by_n_sites_different_donor.png')
fig.clf()

####################
#####################

# ######### Discordant_reads_by_n_sites
##########################

ax1 = sns.violinplot(data=Joined_Df[Joined_Df['Total_sites']<1000], y="Total_sites", x="Nr times becoming different donor in subsampling", cut=0, scale='width')
fig = ax1.get_figure()
fig.savefig('TotalAnalysis__Total_sites_different_donor.png')
fig.clf()

####################
#####################

ax1 = sns.violinplot(data=Joined_Df[Joined_Df['Total_reads']<1000], y="Total_reads", x="Nr times becoming different donor in subsampling", cut=0, scale='width')
fig = ax1.get_figure()
fig.savefig('TotalAnalysis__Total_sites_different_donor.png')
fig.clf()


############ INFORMATIVE SITES VS DONOR HOPS
############################################
Joined_Df2=Joined_Df[Joined_Df['Total_sites']<1000]
ax1 = sns.violinplot(data=Joined_Df2, y="Total_sites", x="Nr times becoming different donor in subsampling", cut=0, scale='width')
fig = ax1.get_figure()
fig.savefig('total_sites_different_donor.png')
fig.clf()
#############################################

############ TOTAL SITES VS DONOR HOPS
############################################
ax1 = sns.violinplot(data=Joined_Df, y="total number of positions cellsp called on", x="Nr times becoming different donor in subsampling", cut=0, scale='width')
fig = ax1.get_figure()
fig.savefig('TOTAL_SITES_different_donor.png')
fig.clf()
###########################

# Joined_Df['informative/total sites called on']=Joined_Df['informative positions cellsp called on']/Joined_Df['total number of positions cellsp called on']
# ax1 = sns.violinplot(data=Joined_Df, y='informative/total sites called on', x="Nr times becoming different donor in subsampling", cut=0, scale='width')
# fig = ax1.get_figure()
# fig.savefig('INF_TOTAL_SITES_different_donor.png')
# fig.clf()


####################
#################### TOTAL vs discordant

fig, ax = plt.subplots(figsize=(6, 6))


sns.scatterplot(
    data=Joined_Df,
    x="Percent_strict_discordant",
    y="total number of sites",
    color="k",label=f"total nr cells assigned to donor={len(Joined_Df)}",
    ax=ax, alpha=0.5
)

# Joined_Df_swap = Joined_Df[Joined_Df['Nr times becoming Unassigned in subsampling']!=0]
# sns.scatterplot(
#     data=Joined_Df_swap,
#     x="Percent_strict_discordant",
#     y="total number of sites",
#     color="b",label=f"becoming Unassigned; total={len(Joined_Df_swap)}",
#     ax=ax, alpha=0.5
# )

# Joined_Df_swap = Joined_Df[Joined_Df['Nr times becoming Doublet in subsampling']!=0]
# sns.scatterplot(
#     data=Joined_Df_swap,
#     x="Percent_strict_discordant",
#     y="total number of sites",
#     color="y", label=f"becoming doublet; total={len(Joined_Df_swap)}",
#     ax=ax, alpha=0.7
# )

Joined_Df_swap = Joined_Df[Joined_Df['Nr times becoming different donor in subsampling']!=0]
Joined_Df_swap = Joined_Df_swap.loc[swap_cohorts_cells]
sns.scatterplot(
    data=Joined_Df_swap,
    x="Percent_strict_discordant",
    y="total number of sites",
    color="r", label=f"becoming different donor; total={len(Joined_Df_swap)}",
    ax=ax,
)
try:
    sns.kdeplot(
        data=Joined_Df_swap,
        x="Percent_strict_discordant",
        y="total number of sites",
        levels=3,
        color='r',
        fill=True,
        alpha=0.6,
        cut=2,
        ax=ax,
    )
except:
    _='only two entris, so cant do a density'

ax.legend()
fig.savefig('prob_max_vs_concordance.png')
fig.clf()

###################
####################



ax1 = sns.violinplot(data=Joined_Df, y="total number of positions cellsp called on", x="Nr times becoming different donor in subsampling", cut=0, scale='width')
fig = ax1.get_figure()
fig.savefig('test3.png')
fig.clf()

ax1 = sns.violinplot(data=Joined_Df, y="Total_reads", x="Nr times becoming different donor in subsampling", cut=0, scale='width')
fig = ax1.get_figure()
fig.savefig('Total_reads_becoming_different_donor.png')
fig.clf()


Joined_Df2 = Joined_Df[Joined_Df["Nr times becoming different donor in subsampling"]!=0]
try:
    ax1 = sns.violinplot(data=Joined_Df2, y="total number of sites", x="Nr times becoming different donor in subsampling", cut=0, scale='width')
    fig = ax1.get_figure()
    fig.savefig('sites_becoming_different_donor_no0.png')
    fig.clf()
except:
    _='There are no cells becoming different donor here.'

try:
    fig.clf()
    ax1 = sns.violinplot(data=Joined_Df2, y="Discordant_reads", x="Nr times becoming different donor in subsampling", cut=0, scale='width')
    fig = ax1.get_figure()
    fig.savefig('Discordant_reads_becoming_different_donor_no0.png')
    fig.clf()
except:
    _='There are no cells becoming different donor here.'    

fig.clf()
ax1 = sns.violinplot(data=Joined_Df, y="Discordant_reads", x="Nr times becoming different donor in subsampling", cut=0, scale='width')
fig = ax1.get_figure()
fig.savefig('Discordant_reads_becoming_different_donor.png')
fig.clf()

fig.clf()
ax1 = sns.violinplot(data=Joined_Df, y="Discordant_reads_by_n_sites", x="Nr times becoming different donor in subsampling", cut=0, scale='width')
fig = ax1.get_figure()
fig.savefig('Discordant_reads_by_n_sites_becoming_different_donor.png')
fig.clf()


fig.clf()
fig, (ax1, ax2) = plt.subplots(1, 2,figsize=(13, 6))
sns.violinplot(data=Joined_Df, y="Nr_concordant_informative", x="Nr times becoming different donor in subsampling", cut=0, scale='width',ax=ax1)
sns.violinplot(data=Joined_Df, y="Nr_discordant_uninformative", x="Nr times becoming different donor in subsampling", cut=0, scale='width',ax=ax2)
fig.savefig('Nr_discordant_uninformative_becoming_different_donor.png')
fig.clf()

try:
    fig.clf()
    ax1 = sns.violinplot(data=Joined_Df2, y="Discordant_reads_by_n_sites", x="Nr times becoming different donor in subsampling", cut=0, scale='width')
    fig = ax1.get_figure()
    fig.savefig('Discordant_reads_by_n_sites_becoming_different_donor_no0.png')
    fig.clf()
except:
    _='There are no cells becoming different donor here.'    

ax1 = sns.violinplot(data=Joined_Df, y="prob_max", x="Nr times becoming different donor in subsampling", cut=0, scale='width')
# ax1 = sns.swarmplot(data=Joined_Df, y="prob_max", x="Nr times becoming different donor in subsampling",color= "white")
fig = ax1.get_figure()
fig.savefig('sites_becoming_different_donor_probs.png')
fig.clf()
ax1 = sns.violinplot(data=Joined_Df, y="Percent_strict_discordant", x="Nr times becoming Unassigned in subsampling", cut=0, scale='width')
fig = ax1.get_figure()
fig.savefig('becoming_unassigned_donor.png')
fig.clf()

ax1 = sns.violinplot(data=Joined_Df, y="total number of sites", x="Nr times becoming different donor in subsampling", cut=0, scale='width')
fig = ax1.get_figure()
fig.savefig('sites_becoming_unassigned_donor.png')
fig.clf()

fig, ax1 = plt.subplots()
ax1 = sns.violinplot(data=Joined_Df, y="Percent_strict_discordant", x="Nr times becoming Doublet in subsampling", cut=0, scale='width')
fig = ax1.get_figure()
fig.savefig('becoming_doublet_donor.png')
ax1.hlines(y=0.2, xmin=0, xmax=20, linewidth=2, color='r')
fig.clf()

ax1 = sns.violinplot(data=Joined_Df, y="total number of sites", x="Nr times becoming different donor in subsampling", cut=0, scale='width')
fig = ax1.get_figure()
fig.savefig('sites_becoming_doublet_donor.png')
fig.clf()

ax1 = sns.violinplot(data=Joined_Df, y="Total_reads", x="Nr times becoming different donor in subsampling", cut=0, scale='width')
fig = ax1.get_figure()
fig.savefig('Total_reads_becoming_different_donor.png')
fig.clf()


def scatter(fig, ax):
    
    sns.scatterplot(
        data=Joined_Df,
        x="Percent_strict_discordant",
        y="total number of sites",
        color="k",label=f"total nr cells assigned to donor={len(Joined_Df)}",
        ax=ax, alpha=0.5
    )

    # Joined_Df_swap = Joined_Df[Joined_Df['Nr times becoming Unassigned in subsampling']!=0]
    # sns.scatterplot(
    #     data=Joined_Df_swap,
    #     x="Percent_strict_discordant",
    #     y="total number of sites",
    #     color="b",label=f"becoming Unassigned; total={len(Joined_Df_swap)}",
    #     ax=ax, alpha=0.5
    # )
    # try:
    #     sns.kdeplot(
    #         data=Joined_Df_swap,
    #         x="Percent_strict_discordant",
    #         y="total number of sites",
    #         levels=2,
    #         color='b',
    #         fill=True,
    #         alpha=0.6,
    #         cut=2,
    #         ax=ax,
    #     )
    # except:
    #     _='only two entris, so cant do a density'

    # Joined_Df_swap = Joined_Df[Joined_Df['Nr times becoming Doublet in subsampling']!=0]
    # sns.scatterplot(
    #     data=Joined_Df_swap,
    #     x="Percent_strict_discordant",
    #     y="total number of sites",
    #     color="y", label=f"becoming doublet; total={len(Joined_Df_swap)}",
    #     ax=ax, alpha=0.7
    # )
    # try:
    #     sns.kdeplot(
    #         data=Joined_Df_swap,
    #         x="Percent_strict_discordant",
    #         y="total number of sites",
    #         levels=2,
    #         color='y',
    #         fill=True,
    #         alpha=0.6,
    #         cut=2,
    #         ax=ax,
    #     )
    # except:
    #     _='only two entris, so cant do a density'

    Joined_Df_swap = Joined_Df[Joined_Df['Nr times becoming different donor in subsampling']!=0]
    
    sns.scatterplot(
        data=Joined_Df_swap,
        x="Percent_strict_discordant",
        y="total number of sites",
        color="r", label=f"becoming different donor; total={len(Joined_Df_swap)}",
        ax=ax,
    )
    try:
        sns.kdeplot(
            data=Joined_Df_swap,
            x="Percent_strict_discordant",
            y="total number of sites",
            levels=3,
            color='r',
            fill=True,
            alpha=0.6,
            cut=2,
            ax=ax,
        )
    except:
        _='only two entris, so cant do a density'
        

    ax.legend()
    return fig

fig, ax = plt.subplots(figsize=(6, 6))
fig = scatter(fig, ax)
fig.savefig('sites_vs_concordance.png')
fig.clf()

try:
    fig, ax = plt.subplots(figsize=(6, 6))
    sns.scatterplot(
        data=Joined_Df,
        y="Percent_strict_discordant",
        x="cell ambientness",
        color="k",label=f"total nr cells assigned to donor={len(Joined_Df)}",
        ax=ax, alpha=0.5
    )
    Joined_Df_swap = Joined_Df[Joined_Df['Nr times becoming different donor in subsampling']!=0]
    sns.scatterplot(
        data=Joined_Df_swap,
        y="Percent_strict_discordant",
        x="cell ambientness",
        color="r", label=f"becoming different donor; total={len(Joined_Df_swap)}",
        ax=ax,
    )

    fig.savefig('ambientness_vs_concordance.png')
    fig.clf()
except:
    _="Ambientness doesnt exist"

try:
    fig, ax = plt.subplots(figsize=(6, 6))
    sns.scatterplot(
        data=Joined_Df,
        y="Discordant_reads",
        x="cell ambientness",
        color="k",label=f"total nr cells assigned to donor={len(Joined_Df)}",
        ax=ax, alpha=0.5
    )
    
    try:
        Joined_Df_swap = Joined_Df[Joined_Df['Tranche Pass/Fail']=='FAIL']
        sns.scatterplot(
            data=Joined_Df_swap,
            y="Discordant_reads",
            x="cell ambientness",
            color="b", label=f"Pool fail",
            ax=ax,
        )
    except:
        _='f'    

    Joined_Df_swap = Joined_Df[Joined_Df['Nr times becoming different donor in subsampling']!=0]
    sns.scatterplot(
        data=Joined_Df_swap,
        y="Discordant_reads",
        x="cell ambientness",
        color="r", label=f"becoming different donor; total={len(Joined_Df_swap)}",
        ax=ax,
    )


    fig.savefig('ambientness_vs_read_concordance.png')
    fig.clf()
except:
    _="Ambientness doesnt exist"

try:
    fig, ax = plt.subplots(figsize=(6, 6))
    sns.scatterplot(
        data=Joined_Df,
        y="Discordant_reads_by_n_sites",
        x="cell ambientness",
        color="k",label=f"total nr cells assigned to donor={len(Joined_Df)}",
        ax=ax, alpha=0.5
    )
    Joined_Df_swap = Joined_Df[Joined_Df['Nr times becoming different donor in subsampling']!=0]
    sns.scatterplot(
        data=Joined_Df_swap,
        y="Discordant_reads_by_n_sites",
        x="cell ambientness",
        color="r", label=f"becoming different donor; total={len(Joined_Df_swap)}",
        ax=ax,
    )

    fig.savefig('ambientness_vs_readbysites_concordance.png')
    fig.clf()
except:
    _="Ambientness doesnt exist"


import math
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable

# Plot of plots, distinguish how many times the cell becomes a different donor
all_sub_times = set(Joined_Df['Nr times becoming different donor in subsampling'])
nr_plots=4
fig, axs = plt.subplots(math.ceil(len(all_sub_times)/2),nr_plots, figsize=(6*2, 6*math.ceil(len(all_sub_times)/2)),gridspec_kw={'width_ratios': [6, 1,6,1]})

st1=-1
st2=-2
all_sub_times=list(all_sub_times)
for i in range(len(all_sub_times)):
    print(i)
    i2=all_sub_times[i]
    if i % 2 == 0:
        # print(f"yes {i}")
        st1+=1
        # st2+=1
        st2=-2   
    st2+=2     
    try:
        ax1=axs[st1, st2]
        ax2=axs[st1, st2+1]
    except:
        ax1=axs[st2]
        ax2=axs[st2+1]

    # print(f"yes [{st1},{st2}]")
    # print(f"yes [{st1},{st2+1}]")
    if i==0:
        scatter(fig, ax1)
        try:
            Joined_Df_swap=Joined_Df[Joined_Df['Nr times becoming different donor in subsampling']!=0]
            Joined_Df_swap['Nr times becoming different donor in subsampling']='at least once'
            sns.violinplot(data=Joined_Df_swap, y="total number of sites", x="Nr times becoming different donor in subsampling", scale='width',ax=ax2,color='r')
        except:
            _='no cells that swap donors'
        continue
    sns.scatterplot(
    data=Joined_Df,
    x="Percent_strict_discordant",
    y="total number of sites",
    color="k",
    ax=ax1, alpha=0.2
    )
    
    Joined_Df_swap = Joined_Df[Joined_Df['Nr times becoming different donor in subsampling']==i2]
    
    try:
        sns.kdeplot(
            data=Joined_Df_swap,
            x="Percent_strict_discordant",
            y="total number of sites",
            levels=3,
            color='r',
            fill=True,
            alpha=0.6,
            cut=2,
            ax=ax1,
        )
    except:
        _='only two entris, so cant do a density'    
    sns.scatterplot(
        data=Joined_Df_swap,
        x="Percent_strict_discordant",
        y="total number of sites",
        color="r",
        ax=ax1, alpha=0.7,label=f"becoming different donor; n={i2}, total={len(Joined_Df_swap)}"
    )

    sns.violinplot(data=Joined_Df_swap, y="total number of sites", x="Nr times becoming different donor in subsampling", scale='width',ax=ax2,color='r')

        
# axs.legend()
fig.tight_layout()
fig.savefig('subplot_sites_vs_concordance.png')
fig.clf()    
print('Done')

