import os
import pandas as pd
import glob
# before merging we need to decrypt the genotype_bridge files using:
# 
def Shipping_Manifests():
    Directory = '/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/ukb_bridge_files/shipping_manifest'
    all_files = glob.glob(f'{Directory}/shipping_manifest*')
    All_Data = pd.DataFrame()
    for bf1 in all_files:
        print(bf1)
        d1 = pd.read_csv(bf1)
        # d1['VACUTAINERID'] = '00'+d1['VACUTAINERID'].astype(str)
        d1['VACUTAINERID'] = d1['VACUTAINERID'].astype(str).str.replace('^0*', '')
        # d1 = d1[['GenotypeEID','VACUTAINERID']]
        # d1.columns = ['oragene_id','s00046_id']
        # d1['s00046_id']='00'+d1['s00046_id'].astype(str)
        # d1['oragene_id']=d1['oragene_id'].astype(str)+'_'+d1['oragene_id'].astype(str)
        All_Data = pd.concat([All_Data,d1])
    All_Data = All_Data.drop_duplicates('VACUTAINERID')
    All_Data.to_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/ukb_bridge_files/shipping_manifest/combined.csv',sep='\t',index=False)

def Bridge_Files():
    Directory = '/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/ukb_bridge_files/genotype_bridge'
    all_files = glob.glob(f'{Directory}/genotyping_bridge*')
    All_Data = pd.DataFrame()
    for bf1 in all_files:
        print(bf1)
        d1 = pd.read_csv(bf1)
        d1 = d1[['GenotypeEID','VACUTAINERID']]
        d1.columns = ['oragene_id','s00046_id']
        d1['s00046_id']='00'+d1['s00046_id'].astype(str)
        d1['oragene_id']=d1['oragene_id'].astype(str)+'_'+d1['oragene_id'].astype(str)
        All_Data = pd.concat([All_Data,d1])
    All_Data['s00046_id'] = All_Data['s00046_id'].str.replace('^0*', '')
    ELGH = pd.read_csv('/lustre/scratch123/hgi/teams/hgi/vvi/2021_11_02_S00046ID_to_OrageneID.txt',sep='\t')
    ELGH2 = pd.read_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/secret/2022_09_27_CARDINAL_datalinkage_deidentified.csv',sep=',')
    ELGH2.oragene_id = ELGH2.oragene_id.str.split('_').str[0]
    ELGH3 = pd.read_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/ELGH/release3/New_Bridge.csv',sep=',', dtype = str)
    ELGH3=ELGH3.rename(columns={'OrageneID_ifnopseudoNHS':'oragene_id'})
    # s00046_id	GSA_oragene
    # S2-999-90054	1544433
    ELGH4=pd.read_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/ELGH/release4/bridge4.csv',sep='\t', dtype = str)
    ELGH4=ELGH4.rename(columns={'GSA_oragene':'oragene_id'})
    cellines = pd.DataFrame([{'s00046_id':'U937','oragene_id':'celline_U937'},{'s00046_id':'THP1','oragene_id':'celline_THP1'}])
    All_Data = pd.concat([All_Data,ELGH,ELGH2,ELGH3,ELGH4,cellines])
    All_Data = All_Data.drop_duplicates()
    All_Data.to_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/secret/bridge.txt',sep='\t',index=False)
    
# Shipping_Manifests()
Bridge_Files()  


# def ronie_try:
#     import pandas as pd
#     data = [{'Gene_st':3,'Gene_end':20}]
#     data.append({'Gene_st':7,'Gene_end':29})
#     dataf = pd.DataFrame(data)
#     dataf['zero_repeats'] =  dataf['Gene_end']-dataf['Gene_st']
#     [0] * dataf['zero_repeats'] [0] 
#     dataf['range']=str([*range(6,19,1)])
#     [*range(6,19,1)]
    
    
print('Done')