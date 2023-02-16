import pandas as pd
import os
import glob
# This code merges all the reports in on file. 
print('lets combine reports')

def Generate_Combined_Reports():
    outdir = "/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/ukbb_handover/reports/2023_15_02"
    All_Tranche_Data = pd.DataFrame()
    UKBB_Reports = pd.DataFrame()
    UKBB_Missing = pd.DataFrame()
    UKBB_Not_Expected = pd.DataFrame()
    all_vcfs = glob.glob(f'/lustre/scratch123/hgi/projects/cardinal_analysis/qc/*/Summary_plots')
    
    all_gems = glob.glob(f'/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/metadata/genestack/gs2/GEMS/*')
    GEMS=pd.DataFrame()
    for g1 in all_gems:
        d1 = pd.read_csv(g1)
        GEMS = pd.concat([GEMS,d1])

    GEMS=GEMS.set_index('Name')
    GEMS_DONORS = GEMS['Sample Source ID'].str.split(',')
    GEMS_DONOR_24h = GEMS['24h'].str.split(',')
    GEMS_DONOR_48h = GEMS['48h'].str.split(',')
    GEMS_DONOR_72h = GEMS['72h'].str.split(',')
    GEMS_DONOR_frozen_h = GEMS['Frozen'].str.split(',')
    
    all_donors_gs = glob.glob(f'/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/metadata/genestack/gs2/meta/*')
    DONS=pd.DataFrame()
    for g1 in all_donors_gs:
        d1 = pd.read_csv(g1)
        DONS = pd.concat([DONS,d1])    
    DONS['Name'] = DONS['Name'].astype(str).str.replace('^0*', '')
    for path in all_vcfs:
        print(path)
        # path='/lustre/scratch123/hgi/projects/cardinal_analysis/qc/Cardinal_46019_Oct_20_2022/Summary_plots'
        Tranche_name = path.split('/')[-2]
            
        Tranche_Data = pd.read_csv(f'{path}/Summary/{Tranche_name}_Tranche_Report.tsv',sep='\t')
        try:
            Donor_Data = pd.read_csv(f'{path}/Summary/UKBB_REPORT/{Tranche_name}_UKBB_Report.tsv',sep='\t')
            Donor_Metadata = pd.read_csv(f'/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/fetch/{Tranche_name}/results/yascp_inputs/Extra_Metadata_Donors.tsv',sep='\t')
            Donor_Metadata['Pool_ID']=Donor_Metadata['experiment_id'].str.split('__').str[0]
            Donor_Metadata['matched_donor_id']=Donor_Metadata['Pool_ID']+'__'+Donor_Metadata['donor']
            Donor_Metadata = Donor_Metadata.drop_duplicates(subset=['matched_donor_id'])
            Donor_Metadata = Donor_Metadata.set_index('matched_donor_id')
            Donor_Data['Vacutainer ID']=Donor_Data['Vacutainer ID'].astype(str)
            Donor_Data['matched_donor_id']=Donor_Data['Pool ID']+'__'+Donor_Data['Vacutainer ID']
            
            Donor_Data = Donor_Data.set_index('matched_donor_id')
            Donor_Metadata.drop_duplicates()
            Donor_Data['Sequencing time']=Donor_Metadata['State']
            # Here need a loop
            
            
            
            Donor_Data['PBMC extraction date']=Donor_Metadata['PBMC extraction date']
            UKBB_Reports = pd.concat([UKBB_Reports,Donor_Data])
            try:
                Missing_Donors = pd.read_csv(f'{path}/Summary/UKBB_REPORT/{Tranche_name}_Missing_UKBB_Donors.tsv',sep='\t')
                UKBB_Missing = pd.concat([UKBB_Missing,Missing_Donors])
            except:
                print('no missing')
            try:
                Not_Expected = pd.read_csv(f'{path}/Summary/UKBB_REPORT/{Tranche_name}_Not_Expected_UKBB_Donors.tsv',sep='\t')
                UKBB_Not_Expected = pd.concat([UKBB_Not_Expected,Not_Expected])
            except:
                print('no missing')
        except:
            print(f'{Tranche_name} doesnt contain UKBB reports')
        All_Tranche_Data = pd.concat([All_Tranche_Data,Tranche_Data])
        print('path')

    UKBB_Reports.loc[UKBB_Reports['PiHat: Expected']== "  ",'PiHat: Expected'] =1
    UKBB_Reports['PiHat: Expected'] = pd.to_numeric(UKBB_Reports['PiHat: Expected']) 
    UKBB_Reports_UKB_0 = UKBB_Reports[~UKBB_Reports['PiHat: Expected'].isnull()] # These are a bit tricky - we dont have pihats for last 4 tranches unfortunatelly.
    UKBB_Reports_UKB_1 = UKBB_Reports[UKBB_Reports['PiHat: Expected'].isnull()] # These are a bit tricky - we dont have pihats for last 4 tranches unfortunatelly.
    
    # UKBB_Reports_UKB_1 = pd.concat([UKBB_Reports_UKB_1,d3])
    UKBB_Reports_UKB_1 = UKBB_Reports_UKB_1.drop_duplicates()
    UKBB_Reports_UKB_1_FIXED =pd.DataFrame()
    
    
    
    for pool in set(UKBB_Reports_UKB_1['Pool ID']):
        all_donor_data = UKBB_Reports_UKB_1[UKBB_Reports_UKB_1['Pool ID']==pool]
        experiment = list(set(UKBB_Reports_UKB_1[UKBB_Reports_UKB_1['Pool ID']==pool]['Experiment ID']))[0]
        GT_Match = pd.read_csv(f'/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc/{experiment}/results_rsync2/results/gtmatch/{pool}/InferedExpected_Expected_Infered_{pool}.genome',sep='\s+')
        input_table = pd.read_csv(f'/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc/{experiment}/results_rsync2/results/handover/Summary_plots/{experiment}/Fetch Pipeline/Input/input_table.tsv',sep='\t')
        input_table = input_table.set_index('experiment_id')
        All_expected = input_table.loc[pool,'donor_vcf_ids']
        Extra_Metadata = pd.read_csv(f'/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/fetch/{experiment}/results/yascp_inputs/Extra_Metadata_Donors.tsv',sep='\t')
        Extra_Metadata['donor'] = Extra_Metadata['donor'].astype(str).str.replace('^0*', '')
        #         Date sample received                                                                   NaN
        # viability                                                                              NaN
        # lab_live_cell_count                                                                    NaN
        # site                                                                                   NaN
        for i,row in all_donor_data.iterrows():
            print(i)
            Donor_id_pre = f"d{row['Pool_ID.Donor_Id'].split('_d')[1]}"
            Donor_id = f"{row['Donor id']}_{row['Donor id']}"
            Vacutainer = row['Vacutainer ID']
            
            M1 = GT_Match[GT_Match['IID1']==Donor_id_pre]
            M2 = GT_Match[GT_Match['IID2']==Donor_id_pre]
            M_COM = pd.concat([M1,M2])
            
            M1 = M_COM[M_COM['IID1']==Donor_id]
            M2 = M_COM[M_COM['IID2']==Donor_id]
            M_COM = pd.concat([M1,M2])
            if (Donor_id=='celline_celline'):
                PIHAT = 1
            else:
                PIHAT = M_COM['PI_HAT'].values[0]
            
            
                all_donor_data.loc[i,'PiHat: Expected']=PIHAT
                all_donor_data.loc[i,'All IDs expected']=All_expected
                Meta = Extra_Metadata[Extra_Metadata['donor']==Vacutainer]
                if len(Meta)>1:
                    # 30007537063
                    
                    chromium = all_donor_data.loc[i,'Chromium channel number']
                    Meta =Meta[Meta['chromium_channel']==chromium]
                    # Meta = Meta[Meta['live_cell_count'] !='0 cells/ml']
                    # if len(Meta)>1:
                    #     Meta = Meta[Meta['State'] == all_donor_data.loc[i,'Sequencing time']]
                    #     if len(Meta)>1:
                    #         Meta = Meta[Meta['live_cell_count'] ==all_donor_data.loc[i,'lab_live_cell_count']]
                try:
                    all_donor_data.loc[i,'Date sample received']=' or '.join(set(Meta['RECIEVED']))
                    all_donor_data.loc[i,'viability']=' or '.join(set(Meta['viability']))
                    all_donor_data.loc[i,'lab_live_cell_count']=' or '.join(set(Meta['live_cell_count']))
                    all_donor_data.loc[i,'site']=' or '.join(set(Meta['SITE']))
                    all_donor_data.loc[i,'amount recieved']=' or '.join(set(Meta['customer_measured_volume'].astype(str)))
                    all_donor_data.loc[i,'Sequencing time']=' or '.join(set(Meta['State'].astype(str)))
                except:
                    print(f'pool {experiment} doesnt contain the metadata')
                all_donor_data.loc[i,'amount recieved']=Meta['customer_measured_volume'].values[0]
        UKBB_Reports_UKB_1_FIXED=pd.concat([UKBB_Reports_UKB_1_FIXED,all_donor_data])
    UKBB_Reports = pd.concat([UKBB_Reports_UKB_0,UKBB_Reports_UKB_1_FIXED])
    
    # second round to add some missing info
    UKBB_Reports_UKB_0 = UKBB_Reports[~UKBB_Reports['All IDs expected'].isnull()]
    UKBB_Reports_UKB_1 = UKBB_Reports[UKBB_Reports['All IDs expected'].isnull()]
    UKBB_Reports_UKB_1_FIXED =pd.DataFrame()
    for pool in set(UKBB_Reports_UKB_1['Pool ID']):
        all_donor_data = UKBB_Reports_UKB_1[UKBB_Reports_UKB_1['Pool ID']==pool]
        experiment = list(set(UKBB_Reports_UKB_1[UKBB_Reports_UKB_1['Pool ID']==pool]['Experiment ID']))[0]
        input_table = pd.read_csv(f'/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc/{experiment}/results_rsync2/results/handover/Summary_plots/{experiment}/Fetch Pipeline/Input/input_table.tsv',sep='\t')
        input_table = input_table.set_index('experiment_id')
        All_expected = input_table.loc[pool,'donor_vcf_ids']
        Extra_Metadata = pd.read_csv(f'/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/fetch/{experiment}/results/yascp_inputs/Extra_Metadata_Donors.tsv',sep='\t')
        Extra_Metadata['donor'] = Extra_Metadata['donor'].astype(str).str.replace('^0*', '')
        #         Date sample received                                                                   NaN
        # viability                                                                              NaN
        # lab_live_cell_count                                                                    NaN
        # site                                                                                   NaN
        for i,row in all_donor_data.iterrows():
            print(i)
            Donor_id_pre = f"d{row['Pool_ID.Donor_Id'].split('_d')[1]}"
            Donor_id = f"{row['Donor id']}_{row['Donor id']}"
            Vacutainer = row['Vacutainer ID']
            
            if (Donor_id=='celline_celline'):
                continue
            else:

                all_donor_data.loc[i,'All IDs expected']=All_expected
                Meta = Extra_Metadata[Extra_Metadata['donor']==Vacutainer]
                
                # try:
                #     if len(Meta)>1:
                #         # 30007537063
                        
                #         chromium = all_donor_data.loc[i,'Chromium channel number']
                #         Meta =Meta[Meta['chromium_channel']==chromium]
                #         # Meta = Meta[Meta['live_cell_count'] !='0 cells/ml']
                #         if len(Meta)>1:
                #             Meta = Meta[Meta['State'] == all_donor_data.loc[i,'Sequencing time']]
                #             # if len(Meta)>1:
                #             #     Meta = Meta[Meta['live_cell_count'] ==all_donor_data.loc[i,'lab_live_cell_count']]
                #         # time = all_donor_data['Sequencing time'].values[0]
                #         # Meta = Meta[Meta['State']==time]
                #     all_donor_data.loc[i,'Date sample received']=Meta['RECIEVED'].values[0]
                #     all_donor_data.loc[i,'viability']=Meta['viability'].values[0]
                #     all_donor_data.loc[i,'lab_live_cell_count']=Meta['live_cell_count'].values[0]
                #     all_donor_data.loc[i,'site']=Meta['SITE'].values[0]
                # except:
                #     print(f'pool {experiment} doesnt contain the metadata')
                # all_donor_data.loc[i,'amount recieved']=Meta['customer_measured_volume'].values[0]
        UKBB_Reports_UKB_1_FIXED=pd.concat([UKBB_Reports_UKB_1_FIXED,all_donor_data])
    UKBB_Reports = pd.concat([UKBB_Reports_UKB_0,UKBB_Reports_UKB_1_FIXED])    
    UKBB_Reports = UKBB_Reports.drop_duplicates()
    # UKBB_Reports[UKBB_Reports['Sequencing time'].isnull()]

    # Fix lab live cell counts
    UKBB_Reports['Antibody batch']='N/A'
    UKBB_Reports['PBMC extraction date']='N/A'
    UKBB_Reports['Conc Pass']='N/A'
    UKBB_Reports['RapidSphere Beads']='N/A'   
    UKBB_Reports['GEM Batch']='N/A'
    
    UKBB_Reports_UKB_0 = UKBB_Reports[~UKBB_Reports['site'].isnull()]
    UKBB_Reports_UKB_1 = UKBB_Reports[UKBB_Reports['site'].isnull()]
    UKBB_Reports_UKB_1 = UKBB_Reports
    UKBB_Reports_UKB_1_FIXED =pd.DataFrame()
    failed_donors=[]
    for pool in set(UKBB_Reports_UKB_1['Pool ID']):
        all_donor_data = UKBB_Reports_UKB_1[UKBB_Reports_UKB_1['Pool ID']==pool]
        experiment = list(set(UKBB_Reports_UKB_1[UKBB_Reports_UKB_1['Pool ID']==pool]['Experiment ID']))[0]
        input_table = pd.read_csv(f'/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc/{experiment}/results_rsync2/results/handover/Summary_plots/{experiment}/Fetch Pipeline/Input/input_table.tsv',sep='\t')
        input_table = input_table.set_index('experiment_id')
        input_table = input_table.drop_duplicates()
        All_expected = input_table.loc[pool,'donor_vcf_ids']
        
        Extra_Metadata = pd.read_csv(f'/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/fetch/{experiment}/results/yascp_inputs/Extra_Metadata_Donors.tsv',sep='\t')
        Extra_Metadata['donor'] = Extra_Metadata['donor'].astype(str).str.replace('^0*', '')
        # Date sample received                                                                   NaN
        # viability                                                                              NaN
        # lab_live_cell_count                                                                    NaN
        # site                                                                                   NaN
        for i,row in all_donor_data.iterrows():
            print(i)
            Donor_id_pre = f"d{row['Pool_ID.Donor_Id'].split('_d')[1]}"
            if (row['Pool_ID.Donor_Id']=='CRD_CMB13195925_donor3'):
                print('yes')
            if (row['Pool_ID.Donor_Id']=='CRD_CMB13195927_donor7'):
                print('yes')
            Donor_id = f"{row['Donor id']}_{row['Donor id']}"
            Vacutainer = row['Vacutainer ID']
            if(Vacutainer=='30007491914'):
                print('this one')
            CC = row['Chromium channel number']
            try:
                LIBRARY_GEMS = GEMS.loc[CC]
                GEM_BATCH = GEMS.loc[CC,'GEMS batch']
                State = GEMS_DONORS.loc[CC]
                index = [idx for idx, s in enumerate(State) if Vacutainer in s][0]
                timing='24h'
                if GEMS_DONOR_24h[CC][index]!='Yes':
                    timing='48h'
                    if GEMS_DONOR_48h[CC][index]!='Yes':
                        timing='72h'
                        if GEMS_DONOR_72h[CC][index]!='Yes':
                            timing='frozen'
                            if GEMS_DONOR_frozen_h[CC][index]!='Yes':
                                timing='N/A'
                donor_data = DONS[DONS['Name'] ==Vacutainer]
                # donor_data = donor_data[donor_data['State']==timing]
                try:
                    State_split = donor_data['State'].values[0].split(',')
                except:
                    State_split = ['dummy']
            except:
                State_split = ['dummy']
                timing='N/A'
                donor_data = DONS[DONS['Name'] ==Vacutainer]
                
            if (len(State_split)>1):
                try:
                    index = [idx for idx, s in enumerate(State_split) if timing in s][0]
                except:
                    failed_donors.append(Vacutainer)
                    continue
                Antibody_batch=donor_data['Antibody batch'].astype(str).values[0].split(',')[index]
                Viability=donor_data['Viability'].astype(str).values[0].split(',')[index]
                Live_cells=donor_data['Live cells'].astype(str).values[0].split(',')[index]
                PBMC_extraction_date=donor_data['PBMC extraction date'].astype(str).values[0].split(',')[index]
                Conc_Pass=donor_data['Conc Pass'].astype(str).values[0].split(',')[index]
                RapidSphere_Beads=donor_data['RapidSphere Beads'].astype(str).values[0].split(',')[index]
                                                
            else:
                Antibody_batch=' or '.join(set(donor_data['Antibody batch'].astype(str)))
                Viability = ' or '.join(set(donor_data['Viability'].astype(str)))
                Live_cells = ' or '.join(set(donor_data['Live cells'].astype(str)))
                PBMC_extraction_date = ' or '.join(set(donor_data['PBMC extraction date'].astype(str)))
                Conc_Pass = ' or '.join(set(donor_data['Conc Pass'].astype(str)))
                RapidSphere_Beads = ' or '.join(set(donor_data['RapidSphere Beads'].astype(str)))
            if (Donor_id=='celline_celline'):
                continue
            else:

                all_donor_data.loc[i,'All IDs expected']=All_expected
                Meta = Extra_Metadata[Extra_Metadata['donor']==Vacutainer]
                
                try:
                    if len(Meta)>1:
                        # 30007537063
                        
                        chromium = all_donor_data.loc[i,'Chromium channel number']
                        Meta =Meta[Meta['chromium_channel']==chromium]
                        # Meta = Meta[Meta['live_cell_count'] !='0 cells/ml']
                        # if len(Meta)>1:
                        #     Meta = Meta[Meta['State'] == all_donor_data.loc[i,'Sequencing time']]
                            # if len(Meta)>1:
                            #     Cell_count = 
                            #     Meta = Meta[Meta['live_cell_count'] ==all_donor_data.loc[i,'lab_live_cell_count']]
                        # time = all_donor_data['Sequencing time'].values[0]
                        # Meta = Meta[Meta['State']==time]
                    viability = ' or '.join(set(Meta['viability']))
                    Recieved = ' or '.join(set(Meta['RECIEVED']))
                    cell_count = ' or '.join(set(Meta['live_cell_count']))
                    site = ' or '.join(set(Meta['SITE']))
                    amount_recieved = ' or '.join(set(Meta['customer_measured_volume'].astype(str)))
                    sequencing_time = ' or '.join(set(Meta['State'].astype(str)))
                    if (timing=='N/A'):
                        timing = sequencing_time
                    if (Viability==''):
                        Viability=viability
                    if (Live_cells==''):
                        Live_cells=cell_count
                    print(f"{Live_cells} vs {cell_count}")
                    print(f"{Viability} vs {viability}")
                    print(f"{timing} vs {sequencing_time}")
                    f"{timing} vs {sequencing_time}"
                    f"{Viability} vs {viability}"
                    f"{Live_cells} vs {cell_count}"

                    all_donor_data.loc[i,'Antibody batch']=Antibody_batch
                    all_donor_data.loc[i,'PBMC extraction date']=PBMC_extraction_date
                    all_donor_data.loc[i,'Conc Pass']=Conc_Pass
                    all_donor_data.loc[i,'RapidSphere Beads']=RapidSphere_Beads
                    all_donor_data.loc[i,'GEM Batch']=GEM_BATCH
                                             
                    all_donor_data.loc[i,'Date sample received']=Recieved
                    all_donor_data.loc[i,'viability']=Viability
                    all_donor_data.loc[i,'lab_live_cell_count']=Live_cells
                    all_donor_data.loc[i,'site']=site
                    all_donor_data.loc[i,'amount recieved']=amount_recieved
                    all_donor_data.loc[i,'Sequencing time']=timing
                except:
                    print(f'pool {experiment} doesnt contain the metadata')
                
        UKBB_Reports_UKB_1_FIXED=pd.concat([UKBB_Reports_UKB_1_FIXED,all_donor_data])
    UKBB_Reports = UKBB_Reports_UKB_1_FIXED
    UKBB_Reports = UKBB_Reports.drop_duplicates()
    print(failed_donors)
    UKBB_Reports.loc[UKBB_Reports['GEM Batch']==20240215,'GEM Batch']=200016416452720240215
    UKBB_Reports.loc[UKBB_Reports['GEM Batch']=='22 Spetember','GEM Batch']='N/A'
    UKBB_Reports['GEM Batch'] = 'GEM:'+UKBB_Reports['GEM Batch'].astype(str)
    UKBB_Reports.loc[UKBB_Reports['GEM Batch']=='GEM:nan','GEM Batch']='GEM:N/A'
    UKBB_Reports['Antibody batch'] = 'AB:'+UKBB_Reports['Antibody batch'].astype(str)
    UKBB_Reports['RapidSphere Beads'] = 'RB:'+UKBB_Reports['RapidSphere Beads'].astype(str)

    # Here we postprocess the data by moving pihats <0.7 to missing and removing tranches with no UKBB samples 
    All_Tranche_Data.to_csv(f'{outdir}/total2/Combined_UKBB_Tranche_Report.tsv',sep='\t',index=False)    
    UKBB_Reports.to_csv(f'{outdir}/total2/Combined_UKBB_Donor_Report.tsv',sep='\t',index=False)
    UKBB_Not_Expected.to_csv(f'{outdir}/total2/Combined_UKBB_Not_Expected.tsv',sep='\t',index=False)
    UKBB_Missing.Sample = UKBB_Missing.Sample.astype(str)
    UKBB_Missing.Sample = UKBB_Missing.Sample.str.replace('\.0','')
    UKBB_Missing = UKBB_Missing.rename(columns={'Pool':'Pool ID','Sample':'Vacutainer ID'})
    UKBB_Missing.to_csv(f'{outdir}/total2/Combined_UKBB_Missing.tsv',sep='\t',index=False)

        
    All_Tranche_Data_UKBB = All_Tranche_Data[All_Tranche_Data['UKB donors expected in pool']!=0]
    # UKBB_Reports['PBMC extraction date'].str.split(' ').str[0].str.split('-').str[2]+UKBB_Reports['PBMC extraction date'].str.split(' ').str[0].str.split('-').str[]
    UKBB_Reports_UKB = UKBB_Reports[UKBB_Reports['PiHat: Expected']>=0.7 ]
    Fail_Pihat_threshold = UKBB_Reports[UKBB_Reports['PiHat: Expected']<0.7]
    Doadgy_pools = UKBB_Reports_UKB[UKBB_Reports_UKB['Pool ID']=='CRD_CMB13303517']
    UKBB_Reports_UKB = UKBB_Reports_UKB[UKBB_Reports_UKB['Pool ID']!='CRD_CMB13303517']
    # We also remove a donors that are in the pool CRD_CMB13303517 as this has some issues of donors mapping to the same id and donors that are missing as part of deconvolutions.
    
    To_Add_to_Missing = Fail_Pihat_threshold[['Pool ID', 'Vacutainer ID']]
    UKBB_Missing_UKBB = pd.concat([UKBB_Missing,To_Add_to_Missing])
    UKBB_Reports_UKB = UKBB_Reports_UKB.rename(columns={'Sequencing time':'Library prep time'})
    UKBB_Reports_UKB = UKBB_Reports_UKB.drop(columns=['PiHat: Expected', 'Infered Relatednes (PiHAT>0.3)','PBMC extraction date','Antibody batch','Conc Pass','RapidSphere Beads'])
    # To_Add_to_Missing.rename(columns={'Pool ID':'Pool','Vacutainer ID':'Sample'})
    Dublicated = UKBB_Reports_UKB[['Vacutainer ID','Overall Pass Fail']][UKBB_Reports_UKB['Vacutainer ID'].duplicated()]
    
    


    THP1 = UKBB_Reports_UKB[UKBB_Reports_UKB['Vacutainer ID']=='THP1']
    U937 = UKBB_Reports_UKB[UKBB_Reports_UKB['Vacutainer ID']=='U937']
    UKBB_DONORS = len(UKBB_Reports_UKB['Vacutainer ID'])-len(THP1)-len(U937)
    print(f"# In total we have {len(set(All_Tranche_Data['Experiment id']))} tranches from which {len(set(All_Tranche_Data_UKBB['Experiment id']))} tranches contain UKBB samples (correspond to sequencing runs). UKBB samples are contained within {len(set(All_Tranche_Data_UKBB['Pool id']))} pools (from which {len(All_Tranche_Data_UKBB[All_Tranche_Data_UKBB['Tranche Pass/Fail']=='PASS'])} pass UKBB pool tresholds). \n \
        # We have {len(UKBB_Reports_UKB['Vacutainer ID'])} reported in total from which {UKBB_DONORS} are UKBB_DONORS donors; {len(THP1)} THP1 spikeins; {len(U937)} U937 spikeins; From these {len(UKBB_Reports_UKB[UKBB_Reports_UKB['Overall Pass Fail']=='PASS'])} pass UKBB donor tresholds \n \
        # {len(set(Dublicated['Vacutainer ID']))-2} Donors are repeated twice - 24h and 48h\n \
        # {len(UKBB_Reports_UKB['Vacutainer ID'])} is a final number after {len(Fail_Pihat_threshold)} donors are moved to missing donors report (as they fail with a pihat<0.7). \n \
        # we also have a pool where 2 deconvoluted donors map to the same expected id with high pihat - this needs to be investigated further - hence {len(Doadgy_pools)} is moved to missing aswell \n \
        # After this move in total we have {len(UKBB_Missing_UKBB)} missing donors as a mostly as a result of low cell recovery and poor libraries or low pihat values matching to expected genotypes or a weird pool. \n \
        # {len(UKBB_Not_Expected)} donors are deconvoluted but are not expected (either by sample swaps in our labs, lims reporting wrong donor pool composition or from ukbb side as matched genotypes are not the ones that have been expected by shipping mannifests ({len(UKBB_Not_Expected[UKBB_Not_Expected['Sample'].str.contains('No_mapping___').fillna(False)])}) with no associated shipping information) \n \
         ")

    UKBB_Missing_UKBB.to_csv(f'{outdir}/ukbb_pihat_processed/Combined_UKBB_Missing.tsv',sep='\t',index=False)
    UKBB_Not_Expected.to_csv(f'{outdir}/ukbb_pihat_processed/Combined_UKBB_Not_Expected.tsv',sep='\t',index=False)
    UKBB_Reports_UKB.to_csv(f'{outdir}/ukbb_pihat_processed/Combined_UKBB_Donor_Report.tsv',sep='\t',index=False)
    All_Tranche_Data_UKBB.to_csv(f'{outdir}/ukbb_pihat_processed/Combined_UKBB_Tranche_Report.tsv',sep='\t',index=False)    
 
    f1 = '/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/ukbb_handover/reports/2023_01_3/ukbb_pihat_processed'
    f2 = '/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/ukbb_handover/reports/2023_15_02/ukbb_pihat_processed'
    Donor_Report_1 = pd.read_csv(f"{f1}/Combined_UKBB_Donor_Report.tsv",sep='\t')
    Donor_Report_2 = pd.read_csv(f"{f2}/Combined_UKBB_Donor_Report.tsv",sep='\t') 
    
    print(f"In previous report provided to UKBB we had {len(Donor_Report_1['Vacutainer ID'])} donors wheres now we have {len(Donor_Report_2['Vacutainer ID'])} donors.")
    print(f"We have {len(set(Donor_Report_2['Vacutainer ID'])-set(Donor_Report_1['Vacutainer ID']))} new donors added and {len(set(Donor_Report_1['Vacutainer ID'])-set(Donor_Report_2['Vacutainer ID']))} donors that are not present in the new report")
    
def Generate_Combined_Reports_ELGH():
    outdir = "/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/ukbb_handover/reports/2023_01_ELGH"
    All_Tranche_Data = pd.DataFrame()
    ELGH_Reports = pd.DataFrame()
    UKBB_Missing = pd.DataFrame()
    UKBB_Not_Expected = pd.DataFrame()
    all_vcfs = glob.glob(f'/lustre/scratch123/hgi/projects/cardinal_analysis/qc/*/Summary_plots')
    for path in all_vcfs:
        print(path)
        # path='/lustre/scratch123/hgi/projects/cardinal_analysis/qc/Cardinal_46019_Oct_20_2022/Summary_plots'
        Tranche_name = path.split('/')[-2]
            
        Tranche_Data = pd.read_csv(f'{path}/Summary/{Tranche_name}_Tranche_Report.tsv',sep='\t')
        try:
            Donor_Data = pd.read_csv(f'{path}/Summary/ELGH_REPORT/{Tranche_name}_ELGH_Report.tsv',sep='\t')
            if len(Donor_Data)==0:
                continue
            Donor_Metadata = pd.read_csv(f'/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/fetch/{Tranche_name}/results/yascp_inputs/Extra_Metadata_Donors.tsv',sep='\t')
            Donor_Metadata['Pool_ID']=Donor_Metadata['experiment_id'].str.split('__').str[0]
            Donor_Metadata['matched_donor_id']=Donor_Metadata['Pool_ID']+'__'+Donor_Metadata['donor']
            Donor_Metadata = Donor_Metadata.drop_duplicates(subset=['matched_donor_id'])
            Donor_Metadata = Donor_Metadata.set_index('matched_donor_id')
            Donor_Data['Vacutainer ID']=Donor_Data['Vacutainer ID'].astype(str)
            Donor_Data['matched_donor_id']=Donor_Data['Pool ID']+'__'+Donor_Data['Vacutainer ID']
            
            Donor_Data = Donor_Data.set_index('matched_donor_id')
            Donor_Metadata.drop_duplicates()
            Donor_Data['Sequencing time']=Donor_Metadata['State']
            # Here need a loop
            
            
            
            Donor_Data['PBMC extraction date']=Donor_Metadata['PBMC extraction date']
            ELGH_Reports = pd.concat([ELGH_Reports,Donor_Data])
            try:
                Missing_Donors = pd.read_csv(f'{path}/Summary/ELGH_REPORT/{Tranche_name}_Missing_UKBB_Donors.tsv',sep='\t')
                UKBB_Missing = pd.concat([UKBB_Missing,Missing_Donors])
            except:
                print('no missing')
            try:
                Not_Expected = pd.read_csv(f'{path}/Summary/ELGH_REPORT/{Tranche_name}_Not_Expected_UKBB_Donors.tsv',sep='\t')
                UKBB_Not_Expected = pd.concat([UKBB_Not_Expected,Not_Expected])
            except:
                print('no missing')
        except:
            print(f'{Tranche_name} doesnt contain UKBB reports')
        All_Tranche_Data = pd.concat([All_Tranche_Data,Tranche_Data])
        print('path')

    ELGH_Reports.loc[ELGH_Reports['PiHat: Expected']== "  ",'PiHat: Expected'] =1
    ELGH_Reports['PiHat: Expected'] = pd.to_numeric(ELGH_Reports['PiHat: Expected']) 
    ELGH_Reports_UKB_0 = ELGH_Reports[~ELGH_Reports['PiHat: Expected'].isnull()] # These are a bit tricky - we dont have pihats for last 4 tranches unfortunatelly.
    ELGH_Reports_UKB_1 = ELGH_Reports[ELGH_Reports['PiHat: Expected'].isnull()] # These are a bit tricky - we dont have pihats for last 4 tranches unfortunatelly.
    
    # ELGH_Reports_UKB_1 = pd.concat([ELGH_Reports_UKB_1,d3])
    ELGH_Reports_UKB_1 = ELGH_Reports_UKB_1.drop_duplicates()
    ELGH_Reports_UKB_1_FIXED =pd.DataFrame()
    
    # ELGH_Reports[ELGH_Reports['Vacutainer ID'].str.contains('S2-057')]
    # ELGH_Reports[ELGH_Reports['Vacutainer ID'].str.contains('S2-046')]
    for pool in set(ELGH_Reports_UKB_1['Pool ID']):
        all_donor_data = ELGH_Reports_UKB_1[ELGH_Reports_UKB_1['Pool ID']==pool]
        try:
            experiment = list(set(ELGH_Reports_UKB_1[ELGH_Reports_UKB_1['Pool ID']==pool]['Experiment ID']))[0]
        except:
            continue
        GT_Match = pd.read_csv(f'/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc/{experiment}/results_rsync2/results/gtmatch/{pool}/InferedExpected_Expected_Infered_{pool}.genome',sep='\s+')
        input_table = pd.read_csv(f'/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc/{experiment}/results_rsync2/results/handover/Summary_plots/{experiment}/Fetch Pipeline/Input/input_table.tsv',sep='\t')
        input_table = input_table.set_index('experiment_id')
        All_expected = input_table.loc[pool,'donor_vcf_ids']
        Extra_Metadata = pd.read_csv(f'/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/fetch/{experiment}/results/yascp_inputs/Extra_Metadata_Donors.tsv',sep='\t')
        Extra_Metadata['donor'] = Extra_Metadata['donor'].astype(str).str.replace('^0*', '')
        #         Date sample received                                                                   NaN
        # viability                                                                              NaN
        # lab_live_cell_count                                                                    NaN
        # site                                                                                   NaN
        for i,row in all_donor_data.iterrows():
            print(i)
            Donor_id_pre = f"d{row['Pool_ID.Donor_Id'].split('_d')[1]}"
            Donor_id = f"{row['Donor id']}_{row['Donor id']}"
            Vacutainer = row['Vacutainer ID']
            
            M1 = GT_Match[GT_Match['IID1']==Donor_id_pre]
            M2 = GT_Match[GT_Match['IID2']==Donor_id_pre]
            M_COM = pd.concat([M1,M2])
            
            M1 = M_COM[M_COM['IID1']==Donor_id]
            M2 = M_COM[M_COM['IID2']==Donor_id]
            M_COM = pd.concat([M1,M2])
            if (Donor_id=='celline_celline'):
                PIHAT = 1
            else:
                PIHAT = M_COM['PI_HAT'].values[0]
            
            
                all_donor_data.loc[i,'PiHat: Expected']=PIHAT
                all_donor_data.loc[i,'All IDs expected']=All_expected
                Meta = Extra_Metadata[Extra_Metadata['donor']==Vacutainer]
                if len(Meta)>1:
                    # 30007537063
                    
                    chromium = all_donor_data.loc[i,'Chromium channel number']
                    Meta =Meta[Meta['chromium_channel']==chromium]
                    # Meta = Meta[Meta['live_cell_count'] !='0 cells/ml']
                    # if len(Meta)>1:
                    #     Meta = Meta[Meta['State'] == all_donor_data.loc[i,'Sequencing time']]
                    #     if len(Meta)>1:
                    #         Meta = Meta[Meta['live_cell_count'] ==all_donor_data.loc[i,'lab_live_cell_count']]
                try:
                    all_donor_data.loc[i,'Date sample received']=' or '.join(set(Meta['RECIEVED']))
                    all_donor_data.loc[i,'viability']=' or '.join(set(Meta['viability']))
                    all_donor_data.loc[i,'lab_live_cell_count']=' or '.join(set(Meta['live_cell_count']))
                    all_donor_data.loc[i,'site']=' or '.join(set(Meta['SITE']))
                    all_donor_data.loc[i,'amount recieved']=' or '.join(set(Meta['customer_measured_volume'].astype(str)))
                    all_donor_data.loc[i,'Sequencing time']=' or '.join(set(Meta['State'].astype(str)))
                except:
                    print(f'pool {experiment} doesnt contain the metadata')
                all_donor_data.loc[i,'amount recieved']=Meta['customer_measured_volume'].values[0]
        ELGH_Reports_UKB_1_FIXED=pd.concat([ELGH_Reports_UKB_1_FIXED,all_donor_data])
    ELGH_Reports = pd.concat([ELGH_Reports_UKB_0,ELGH_Reports_UKB_1_FIXED])
    
    # second round to add some missing info
    ELGH_Reports_UKB_0 = ELGH_Reports[~ELGH_Reports['All IDs expected'].isnull()]
    ELGH_Reports_UKB_1 = ELGH_Reports[ELGH_Reports['All IDs expected'].isnull()]
    ELGH_Reports_UKB_1_FIXED =pd.DataFrame()
    for pool in set(ELGH_Reports_UKB_1['Pool ID']):
        all_donor_data = ELGH_Reports_UKB_1[ELGH_Reports_UKB_1['Pool ID']==pool]
        experiment = list(set(ELGH_Reports_UKB_1[ELGH_Reports_UKB_1['Pool ID']==pool]['Experiment ID']))[0]
        input_table = pd.read_csv(f'/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc/{experiment}/results_rsync2/results/handover/Summary_plots/{experiment}/Fetch Pipeline/Input/input_table.tsv',sep='\t')
        input_table = input_table.set_index('experiment_id')
        All_expected = input_table.loc[pool,'donor_vcf_ids']
        Extra_Metadata = pd.read_csv(f'/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/fetch/{experiment}/results/yascp_inputs/Extra_Metadata_Donors.tsv',sep='\t')
        Extra_Metadata['donor'] = Extra_Metadata['donor'].astype(str).str.replace('^0*', '')
        #         Date sample received                                                                   NaN
        # viability                                                                              NaN
        # lab_live_cell_count                                                                    NaN
        # site                                                                                   NaN
        for i,row in all_donor_data.iterrows():
            print(i)
            Donor_id_pre = f"d{row['Pool_ID.Donor_Id'].split('_d')[1]}"
            Donor_id = f"{row['Donor id']}_{row['Donor id']}"
            Vacutainer = row['Vacutainer ID']
            
            if (Donor_id=='celline_celline'):
                continue
            else:

                all_donor_data.loc[i,'All IDs expected']=All_expected
                Meta = Extra_Metadata[Extra_Metadata['donor']==Vacutainer]
                
                # try:
                #     if len(Meta)>1:
                #         # 30007537063
                        
                #         chromium = all_donor_data.loc[i,'Chromium channel number']
                #         Meta =Meta[Meta['chromium_channel']==chromium]
                #         # Meta = Meta[Meta['live_cell_count'] !='0 cells/ml']
                #         if len(Meta)>1:
                #             Meta = Meta[Meta['State'] == all_donor_data.loc[i,'Sequencing time']]
                #             # if len(Meta)>1:
                #             #     Meta = Meta[Meta['live_cell_count'] ==all_donor_data.loc[i,'lab_live_cell_count']]
                #         # time = all_donor_data['Sequencing time'].values[0]
                #         # Meta = Meta[Meta['State']==time]
                #     all_donor_data.loc[i,'Date sample received']=Meta['RECIEVED'].values[0]
                #     all_donor_data.loc[i,'viability']=Meta['viability'].values[0]
                #     all_donor_data.loc[i,'lab_live_cell_count']=Meta['live_cell_count'].values[0]
                #     all_donor_data.loc[i,'site']=Meta['SITE'].values[0]
                # except:
                #     print(f'pool {experiment} doesnt contain the metadata')
                # all_donor_data.loc[i,'amount recieved']=Meta['customer_measured_volume'].values[0]
        ELGH_Reports_UKB_1_FIXED=pd.concat([ELGH_Reports_UKB_1_FIXED,all_donor_data])
    ELGH_Reports = pd.concat([ELGH_Reports_UKB_0,ELGH_Reports_UKB_1_FIXED])    
    ELGH_Reports = ELGH_Reports.drop_duplicates()
    # ELGH_Reports[ELGH_Reports['Sequencing time'].isnull()]

    # Fix lab live cell counts
    ELGH_Reports_UKB_0 = ELGH_Reports[~ELGH_Reports['site'].isnull()]
    ELGH_Reports_UKB_1 = ELGH_Reports[ELGH_Reports['site'].isnull()]
    ELGH_Reports_UKB_1 = ELGH_Reports
    ELGH_Reports_UKB_1_FIXED =pd.DataFrame()
    for pool in set(ELGH_Reports_UKB_1['Pool ID']):
        all_donor_data = ELGH_Reports_UKB_1[ELGH_Reports_UKB_1['Pool ID']==pool]
        experiment = list(set(ELGH_Reports_UKB_1[ELGH_Reports_UKB_1['Pool ID']==pool]['Experiment ID']))[0]
        input_table = pd.read_csv(f'/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc/{experiment}/results_rsync2/results/handover/Summary_plots/{experiment}/Fetch Pipeline/Input/input_table.tsv',sep='\t')
        input_table = input_table.set_index('experiment_id')
        input_table = input_table.drop_duplicates()
        All_expected = input_table.loc[pool,'donor_vcf_ids']
        
        Extra_Metadata = pd.read_csv(f'/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/fetch/{experiment}/results/yascp_inputs/Extra_Metadata_Donors.tsv',sep='\t')
        Extra_Metadata['donor'] = Extra_Metadata['donor'].astype(str).str.replace('^0*', '')
        #         Date sample received                                                                   NaN
        # viability                                                                              NaN
        # lab_live_cell_count                                                                    NaN
        # site                                                                                   NaN
        for i,row in all_donor_data.iterrows():
            print(i)
            Donor_id_pre = f"d{row['Pool_ID.Donor_Id'].split('_d')[1]}"
            if (row['Pool_ID.Donor_Id']=='CRD_CMB13195925_donor3'):
                print('yes')
            if (row['Pool_ID.Donor_Id']=='CRD_CMB13195927_donor7'):
                print('yes')
            Donor_id = f"{row['Donor id']}_{row['Donor id']}"
            Vacutainer = row['Vacutainer ID']
            
            if (Donor_id=='celline_celline'):
                continue
            else:

                all_donor_data.loc[i,'All IDs expected']=All_expected
                Meta = Extra_Metadata[Extra_Metadata['donor']==Vacutainer]
                
                try:
                    if len(Meta)>1:
                        # 30007537063
                        
                        chromium = all_donor_data.loc[i,'Chromium channel number']
                        Meta =Meta[Meta['chromium_channel']==chromium]
                        # Meta = Meta[Meta['live_cell_count'] !='0 cells/ml']
                        # if len(Meta)>1:
                        #     Meta = Meta[Meta['State'] == all_donor_data.loc[i,'Sequencing time']]
                            # if len(Meta)>1:
                            #     Cell_count = 
                            #     Meta = Meta[Meta['live_cell_count'] ==all_donor_data.loc[i,'lab_live_cell_count']]
                        # time = all_donor_data['Sequencing time'].values[0]
                        # Meta = Meta[Meta['State']==time]
                    all_donor_data.loc[i,'Date sample received']=' or '.join(set(Meta['RECIEVED']))
                    all_donor_data.loc[i,'viability']=' or '.join(set(Meta['viability']))
                    all_donor_data.loc[i,'lab_live_cell_count']=' or '.join(set(Meta['live_cell_count']))
                    all_donor_data.loc[i,'site']=' or '.join(set(Meta['SITE']))
                    all_donor_data.loc[i,'amount recieved']=' or '.join(set(Meta['customer_measured_volume'].astype(str)))
                    all_donor_data.loc[i,'Sequencing time']=' or '.join(set(Meta['State'].astype(str)))
                except:
                    print(f'pool {experiment} doesnt contain the metadata')
                
        ELGH_Reports_UKB_1_FIXED=pd.concat([ELGH_Reports_UKB_1_FIXED,all_donor_data])
    ELGH_Reports = ELGH_Reports_UKB_1_FIXED
    ELGH_Reports = ELGH_Reports.drop_duplicates()
        

    


    
    # Here we postprocess the data by moving pihats <0.7 to missing and removing tranches with no UKBB samples 
    All_Tranche_Data.to_csv(f'{outdir}/total2/Combined_UKBB_Tranche_Report.tsv',sep='\t',index=False)    
    ELGH_Reports.to_csv(f'{outdir}/total2/Combined_UKBB_Donor_Report.tsv',sep='\t',index=False)
    UKBB_Not_Expected.to_csv(f'{outdir}/total2/Combined_UKBB_Not_Expected.tsv',sep='\t',index=False)
    UKBB_Missing.Sample = UKBB_Missing.Sample.astype(str)
    UKBB_Missing.Sample = UKBB_Missing.Sample.str.replace('\.0','')
    UKBB_Missing = UKBB_Missing.rename(columns={'Pool':'Pool ID','Sample':'Vacutainer ID'})
    UKBB_Missing.to_csv(f'{outdir}/total2/Combined_UKBB_Missing.tsv',sep='\t',index=False)

        
    All_Tranche_Data_UKBB = All_Tranche_Data[All_Tranche_Data['UKB donors expected in pool']!=0]
    # ELGH_Reports['PBMC extraction date'].str.split(' ').str[0].str.split('-').str[2]+ELGH_Reports['PBMC extraction date'].str.split(' ').str[0].str.split('-').str[]
    ELGH_Reports_UKB = ELGH_Reports[ELGH_Reports['PiHat: Expected']>=0.7 ]
    Fail_Pihat_threshold = ELGH_Reports[ELGH_Reports['PiHat: Expected']<0.7]
    Doadgy_pools = ELGH_Reports_UKB[ELGH_Reports_UKB['Pool ID']=='CRD_CMB13303517']
    ELGH_Reports_UKB = ELGH_Reports_UKB[ELGH_Reports_UKB['Pool ID']!='CRD_CMB13303517']
    # We also remove a donors that are in the pool CRD_CMB13303517 as this has some issues of donors mapping to the same id and donors that are missing as part of deconvolutions.
    
    To_Add_to_Missing = Fail_Pihat_threshold[['Pool ID', 'Vacutainer ID']]
    UKBB_Missing_UKBB = pd.concat([UKBB_Missing,To_Add_to_Missing])
    ELGH_Reports_UKB = ELGH_Reports_UKB.rename(columns={'Sequencing time':'Library prep time'})
    ELGH_Reports_UKB = ELGH_Reports_UKB.drop(columns=['PiHat: Expected', 'Infered Relatednes (PiHAT>0.3)','PBMC extraction date','Antibody batch','Conc Pass','RapidSphere Beads'])
    # To_Add_to_Missing.rename(columns={'Pool ID':'Pool','Vacutainer ID':'Sample'})
    Dublicated = ELGH_Reports_UKB[['Vacutainer ID','Overall Pass Fail']][ELGH_Reports_UKB['Vacutainer ID'].duplicated()]
    
    


    THP1 = ELGH_Reports_UKB[ELGH_Reports_UKB['Vacutainer ID']=='THP1']
    U937 = ELGH_Reports_UKB[ELGH_Reports_UKB['Vacutainer ID']=='U937']
    UKBB_DONORS = len(ELGH_Reports_UKB['Vacutainer ID'])-len(THP1)-len(U937)
    print(f"# In total we have {len(set(All_Tranche_Data['Experiment id']))} tranches from which {len(set(All_Tranche_Data_UKBB['Experiment id']))} tranches contain UKBB samples (correspond to sequencing runs). UKBB samples are contained within {len(set(All_Tranche_Data_UKBB['Pool id']))} pools (from which {len(All_Tranche_Data_UKBB[All_Tranche_Data_UKBB['Tranche Pass/Fail']=='PASS'])} pass UKBB pool tresholds). \n \
        # We have {len(ELGH_Reports_UKB['Vacutainer ID'])} reported in total from which {UKBB_DONORS} are UKBB_DONORS donors; {len(THP1)} THP1 spikeins; {len(U937)} U937 spikeins; From these {len(ELGH_Reports_UKB[ELGH_Reports_UKB['Overall Pass Fail']=='PASS'])} pass UKBB donor tresholds \n \
        # {len(set(Dublicated['Vacutainer ID']))-2} Donors are repeated twice - 24h and 48h\n \
        # {len(ELGH_Reports_UKB['Vacutainer ID'])} is a final number after {len(Fail_Pihat_threshold)} donors are moved to missing donors report (as they fail with a pihat<0.7). \n \
        # we also have a pool where 2 deconvoluted donors map to the same expected id with high pihat - this needs to be investigated further - hence {len(Doadgy_pools)} is moved to missing aswell \n \
        # After this move in total we have {len(UKBB_Missing_UKBB)} missing donors as a mostly as a result of low cell recovery and poor libraries or low pihat values matching to expected genotypes or a weird pool. \n \
        # {len(UKBB_Not_Expected)} donors are deconvoluted but are not expected (either by sample swaps in our labs, lims reporting wrong donor pool composition or from ukbb side as matched genotypes are not the ones that have been expected by shipping mannifests ({len(UKBB_Not_Expected[UKBB_Not_Expected['Sample'].str.contains('No_mapping___').fillna(False)])}) with no associated shipping information) \n \
         ")

    UKBB_Missing_UKBB.to_csv(f'{outdir}/ukbb_pihat_processed/Combined_UKBB_Missing.tsv',sep='\t',index=False)
    UKBB_Not_Expected.to_csv(f'{outdir}/ukbb_pihat_processed/Combined_UKBB_Not_Expected.tsv',sep='\t',index=False)
    ELGH_Reports_UKB.to_csv(f'{outdir}/ukbb_pihat_processed/Combined_UKBB_Donor_Report.tsv',sep='\t',index=False)
    All_Tranche_Data_UKBB.to_csv(f'{outdir}/ukbb_pihat_processed/Combined_UKBB_Tranche_Report.tsv',sep='\t',index=False)    
 
    f1 = '/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/ukbb_handover/reports/2022_11/ukbb_pihat_processed'
    f2 = '/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/ukbb_handover/reports/2023_01/ukbb_pihat_processed'
    Donor_Report_1 = pd.read_csv(f"{f1}/Combined_UKBB_Donor_Report.tsv",sep='\t')
    Donor_Report_2 = pd.read_csv(f"{f2}/Combined_UKBB_Donor_Report.tsv",sep='\t') 
    
    print(f"In previous report provided to UKBB we had {len(Donor_Report_1['Vacutainer ID'])} donors wheres now we have {len(Donor_Report_2['Vacutainer ID'])} donors.")
    print(f"We have {len(set(Donor_Report_2['Vacutainer ID'])-set(Donor_Report_1['Vacutainer ID']))} new donors added and {len(set(Donor_Report_1['Vacutainer ID'])-set(Donor_Report_2['Vacutainer ID']))} donors that are not present in the new report")
   

def compare_produced_reports():
    print('Do')
    f1 = '/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/ukbb_handover/reports/2023_01/total'
    f2 = '/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/ukbb_handover/reports/2023_01/total2'
    
    Donor_Report_1 = pd.read_csv(f"{f1}/Combined_UKBB_Donor_Report.tsv",sep='\t')
    Donor_Report_2 = pd.read_csv(f"{f2}/Combined_UKBB_Donor_Report.tsv",sep='\t')

    print('Done')
Generate_Combined_Reports()
