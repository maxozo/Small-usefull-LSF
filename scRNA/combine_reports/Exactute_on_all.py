import os
import glob
import pandas as pd

def update_all_metadata():
    all_vcfs = glob.glob(f'/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/fetch/*/results/yascp_inputs/Update_Extra_Metadata.sh')
    for path in all_vcfs:
        print(path)
        path1='/'.join(path.split('/')[:-1])
        os.system(f"cd {path1} && cp Extra_Metadata_Donors.tsv Extra_Metadata_Donors_old1.tsv && cp Extra_Metadata.tsv Extra_Metadata_old1.tsv && bash Update_Extra_Metadata.sh")
            
def add_extraction_date_to_reports():
    # This was used to extract all the timings from Stephens metadata to add to the YASCP input files.
    All_Concentrated_Lab_Metadata = pd.read_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/metadata/metadata_merged_16_03_2023.tsv',sep='\t')
    All_Concentrated_Lab_Metadata = All_Concentrated_Lab_Metadata.set_index('Cellaca ID')
    all_vcfs = glob.glob(f'/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/fetch/*/results/yascp_inputs/Extra_Metadata_Donors.tsv')
    all_unnown = []
    # gem_batch_data = pd.read_csv("/lustre/scratch123/hgi/projects/cardinal_analysis/analysis/common_files/metadata/GEM_metadata_merged.tsv",sep='\t')
    for path in all_vcfs:  
        # path=f'/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/fetch/Cardinal_46019_Oct_20_2022/results/yascp_inputs/Extra_Metadata_Donors.tsv'
        Tranche_Data_path = '/'.join(path.split('/')[:-1])
        Tranche_Data_path=pd.read_csv(f'{Tranche_Data_path}/Extra_Metadata.tsv',sep='\t')
        Pool = path.split('/')[-4]
        D1 = pd.read_csv(path,sep='\t')
        if (Pool=='Blood_Fresh'):
            continue
        try:
            D1.donor=D1.donor.str.replace('^0*', '')
        except:
            continue
        All_Concentrated_Lab_Metadata['SAMPLE BARCODE']=All_Concentrated_Lab_Metadata['SAMPLE BARCODE'].str.replace('^0*', '')
        D1['State']=''
        D1['PBMC extraction date']=''
        for i1,don1_row in D1.iterrows():
            if (don1_row['donor'] =='30007454087'):
                print('yes')
            Tr1 = Tranche_Data_path[Tranche_Data_path['chromium_channel']==don1_row['chromium_channel']]
            Experiment = Tr1['experiment_id'].values[0]
            # print(don1_row)
            record=True
            try:
                donor_lims_id = don1_row['id_pool_lims']
            except:
                donor_lims_id = Tr1['public_name'].values[0]
            chrom_chan = don1_row['chromium_channel']
            chrom_chan_id = chrom_chan.split(':')[0]
            # Gem_Batch = gem_batch_data[gem_batch_data['Chromium channel number']==chrom_chan]
            # Don_GEM = Gem_Batch['Vacutainer ID']==don1_row['donor']
            # LCA Connect PCRXP
            donor = don1_row['donor']
            if ('THP1' not in donor and 'U937' not in donor):
                try:
                    Donor_vars = All_Concentrated_Lab_Metadata.loc[donor_lims_id]
                    D1.loc[i1,'PBMC extraction date']=Donor_vars['PBMC extraction date ']
                    D1.loc[i1,'State']=Donor_vars['State']
                except:
                    Donor_vars_Pre = All_Concentrated_Lab_Metadata[All_Concentrated_Lab_Metadata['SAMPLE BARCODE']==donor]
                    Donor_vars = Donor_vars_Pre
                    if(len(Donor_vars)>1):
                        try:
                            Donor_vars = Donor_vars[Donor_vars['LCA_PBMC']==donor_lims_id.split(':')[0]]
                            if(len(Donor_vars)<1):
                                Donor_vars = Donor_vars_Pre[Donor_vars_Pre.index==donor_lims_id]
                                if(len(Donor_vars)<1):
                                    # Here there is an ambiguity in which is the corect donor as the ids dont match
                                    record=False
                                    all_unnown.append({'Tranche':Pool,'Experiment':Experiment,'Donor lims ID':donor_lims_id, 'Donor':donor,'Chromium Chanel':chrom_chan,'Possible Cellaca IDs':';'.join(Donor_vars_Pre.index), 'Possible LC BLOOD ARRAYS':';'.join(Donor_vars_Pre['LCA_PBMC']),'Possible LCA PBMC Pools':';'.join(Donor_vars_Pre['LCA PBMC Pools']),'reasoning':'Ids between LIMS and Metadata do not match'})
                                    print(f'breaking: {donor}')
                        except:
                            all_unnown.append({'Tranche':Pool,'Experiment':Experiment,'Donor lims ID':donor_lims_id, 'Donor':donor,'Chromium Chanel':chrom_chan,'Possible Cellaca IDs':';'.join(Donor_vars_Pre.index.astype(str)), 'Possible LC BLOOD ARRAYS':';'.join(Donor_vars_Pre['LCA_PBMC']),'Possible LCA PBMC Pools':';'.join(Donor_vars_Pre['LCA PBMC Pools']),'reasoning':'Ids between LIMS and Metadata do not match'})
                            print(f'breaking: {donor}')
                    elif len(Donor_vars)<1:
                        # Here we dont find the DOnor at all in metadata
                        record=False
                        all_unnown.append({'Tranche':Pool,'Experiment':Experiment,'Donor lims ID':donor_lims_id, 'Donor':donor,'Chromium Chanel':chrom_chan,'Possible Cellaca IDs':';'.join(Donor_vars_Pre.index), 'Possible LC BLOOD ARRAYS':';'.join(Donor_vars_Pre['LCA_PBMC']),'Possible LCA PBMC Pools':';'.join(Donor_vars_Pre['LCA PBMC Pools']),'reasoning':'Donot Missing from Metadata'})
                        print(f'breaking: {donor}')                       
                    if record:        
                        D1.loc[i1,'PBMC extraction date']=Donor_vars['PBMC extraction date '].values[0]
                        D1.loc[i1,'State']=Donor_vars['State'].values[0]
        if (not os.path.exists(f'{path}.old')):
            os.system(f'cp {path} {path}.old')
        D1.to_csv(path,sep='\t',index=False)
    All_Failed = pd.DataFrame(all_unnown)
    All_Failed.to_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/metadata/Failed_To_Determine_time.tsv',sep='\t')

def get_total_cell_compositions():
    import pandas as pd
    import glob
    import os
    # os.getcwd()
    
    # #1 Step - extract all the var objects in each of the h5ad files and save them
    # all_vcfs = glob.glob(f'/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc/*/results_rsync2/results/adata.h5ad')

    # for path in all_vcfs:
    #     print(path)
    #     adata = sc.read_h5ad(filename=path)
    #     Out_file = '/'.join(path.split('/')[:-1])
    #     adata.var.to_csv(f"{Out_file}/adata_var.tsv",sep='\t')
    #     del adata    
    
    
    # #2 Step - Merge all the var objects together in one file
    # all_vcfs = glob.glob(f'/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc/*/results_rsync2/results/adata_obs.tsv')

    # Data_All = pd.DataFrame()
    # count=0
    # for path in all_vcfs:
    #     count+=1
    #     print(count)
    #     print(path)
    #     p2 = '/'.join(path.split('/')[:-1])
    #     Data_QC = pd.read_csv(path,sep='\t',index_col=0)
    #     Celltype = pd.read_csv(f"{p2}/celltype/All_Celltype_Assignments.csv",sep='\t',index_col=0)
    #     Data_QC['Azimuth l2'] = Celltype['Azimuth:predicted.celltype.l2']
    #     Data_QC[Data_QC['cell_passes_qc'] ==True]['Azimuth l2'].value_counts()
    #     Data_All= pd.concat([Data_All,Data_QC])

    # Data_All.to_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc/Merged_Obs.tsv',sep='\t')
    
    # #3 Step - Count all the failed and passed cells
    # Data_All = pd.read_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc/Merged_Obs.tsv',sep='\t',index_col=0)
    # val_counts_all = Data_All['Azimuth l2'].value_counts()
    # val_counts_passqc = Data_All[Data_All['cell_passes_qc'] ==True]['Azimuth l2'].value_counts()
    # val_counts_failqc = Data_All[Data_All['cell_passes_qc'] ==False]['Azimuth l2'].value_counts()

    # val_counts_failqc.to_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc/val_counts_failqc.tsv',sep='\t')
    # val_counts_passqc.to_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc/val_counts_passqc.tsv',sep='\t')
    # val_counts_all.to_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc/val_counts_all.tsv',sep='\t')

    # #4 Step - generate an output file that lists the combined fails and passes
    Data1 = pd.read_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc/val_counts_failqc.tsv',sep='\t',index_col=0)
    Data2 = pd.read_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc/val_counts_passqc.tsv',sep='\t',index_col=0)
    Data3 = pd.read_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc/val_counts_all.tsv',sep='\t',index_col=0)

    Data1=Data1.rename(columns={'Azimuth l2':'fails qc'})
    Data2=Data2.rename(columns={'Azimuth l2':'passes qc'})
    Data3=Data3.rename(columns={'Azimuth l2':'all cell nr'})


    Combined = pd.concat([Data3,Data2,Data1],axis=1)
    Combined['percent passing qc']= Combined['passes qc']/Combined['all cell nr']*100
    Combined.to_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc/total_cell_counts_per_celltype.tsv',sep='\t')
    Combined['passes qc']+Combined['fails qc']
    print(done)
        
def combine_all_meta():
    # This is used to combine all Stephens metadata reports in one file that is later on utilised to determine the PBMC extraction date and the time of sequencing.
    all_vcfs = glob.glob(f'/nfs/team151/CARDINAL/*/*eta_*.xl*')
    All_META = pd.DataFrame()
    for xl1 in all_vcfs:
        print(xl1)
        # xl1 = "/nfs/team151/CARDINAL/12_12_20/Meta_data_121222.xlsm"
        if (xl1.split('/')[-1][0]!='~'):
            D1 = pd.read_excel(xl1,sheet_name='LCA_PBMC')
            D2 = D1.dropna(subset=['SAMPLE BARCODE'])
            All_META=pd.concat([All_META,D2])
        else:
            print(f"fail:{xl1}")  
    All_META.to_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/metadata/metadata_merged_16_03_2023.tsv',sep='\t')
add_extraction_date_to_reports()
# combine_all_meta()
print('Done')