import pandas as pd
import os
import glob
# This code compares the number of cells identified for the same donor between two independent methods and calculates the overlap percentage.
print('lets combine reports')


all_vcfs = glob.glob(f'/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc/*/results_vireo_inp/results/deconvolution/vireo_gt_fix/assignments_all_pools.tsv')
All_Tranche_Data = pd.DataFrame()
Dataset_nr_comparisons = {}
for path in all_vcfs:
    try:
        Tranche_path = f"/{os.path.join(*path.split('/')[:-5])}"
        # Vireo_Expected_pihats_Data = pd.read_csv(path,sep='\t')
        Assignments_file =  pd.read_csv(f"{Tranche_path}/results_rsync2/results/deconvolution/vireo_gt_fix/assignments_all_pools.tsv",sep='\t')
        Assignments_file_expectd = Assignments_file[Assignments_file['Match Expected'] == True]
        Vireo_Assignments_file =  pd.read_csv(path,sep='\t')
        Vireo_Assignments_file_expectd = Vireo_Assignments_file[Vireo_Assignments_file['Match Expected'] == True]
        Vireo_Assignments_file_expectd['donor_pool']= Vireo_Assignments_file_expectd['donor_gt']+'___'+Vireo_Assignments_file_expectd['pool']
        Assignments_file_expectd['donor_pool']= Assignments_file_expectd['donor_gt']+'___'+Assignments_file_expectd['pool']
        Vireo_Assignments_file_expectd['donor_pool']=Vireo_Assignments_file_expectd['donor_pool'].str.replace('celline_','')
        All_Donors_Deconvoluted_Expected = set(Assignments_file_expectd['donor_pool']).union(set(Vireo_Assignments_file_expectd['donor_pool']))
        
        for id1 in All_Donors_Deconvoluted_Expected:
            sp1 = id1.split('___')
            pool1 = sp1[1]
            donor1 = sp1[0]
            
            Assignments_nr = pd.read_csv(f"{Tranche_path}/results_rsync2/results/deconvolution/vireo_gt_fix/{pool1}/GT_replace_{pool1}__exp.sample_summary.txt",sep='\t',header=None) 
            Cell_IDs =  pd.read_csv(f"{Tranche_path}/results_rsync2/results/deconvolution/vireo_gt_fix/{pool1}/GT_replace_donor_ids.tsv",sep='\t') 
            
            try:
                donor_nr = Assignments_file_expectd[Assignments_file_expectd['donor_pool']==id1]['donor_query'].values[0]
                Nr_cells = Assignments_nr[Assignments_nr.iloc[:,0].str.contains(donor1)][1].values[0]
                Cell_IDs_don = set(Cell_IDs[Cell_IDs['donor_id'].str.contains(donor1)]['cell'])
                
            except:
                Nr_cells = None
                Cell_IDs_don=set([])
            
            Vireo_Assignments_nr = pd.read_csv(f"{Tranche_path}/results_vireo_inp/results/deconvolution/vireo_gt_fix/{pool1}/GT_replace_{pool1}__exp.sample_summary.txt",sep='\t',header=None) 
            Vireo_Cell_IDs =  pd.read_csv(f"{Tranche_path}/results_vireo_inp/results/deconvolution/vireo_gt_fix/{pool1}/GT_replace_donor_ids.tsv",sep='\t') 
            
            try:
                donor_nr_vireo = Vireo_Assignments_file_expectd[Vireo_Assignments_file_expectd['donor_pool']==id1]['donor_query'].values[0]
                Vireo_Nr_cells = Vireo_Assignments_nr[Vireo_Assignments_nr.iloc[:,0].str.contains(donor1)][1].values[0]
                Vireo_Cell_IDs_don = set(Vireo_Cell_IDs[Vireo_Cell_IDs['donor_id'].str.contains(donor1)]['cell'])
            except:
                Vireo_Nr_cells = None
                Vireo_Cell_IDs_don=set([])
            print(f"{Vireo_Nr_cells} vs {Nr_cells}")
            Overlap = len(set(Vireo_Cell_IDs_don)&set(Cell_IDs_don)) / float(len(set(Vireo_Cell_IDs_don) | set(Cell_IDs_don))) * 100
            Dataset_nr_comparisons[id1]={'Vireo with GT nr cells':Vireo_Nr_cells, 'Vireo nr cells (discovery)':Nr_cells,'Cell ID overlap %': Overlap}
    except:
        print('Not available')
d3 = pd.DataFrame(Dataset_nr_comparisons).T
d3.to_csv('/lustre/scratch123/hgi/projects/cardinal_analysis/analysis/mo11/cell_nr_differences_vireo_with_GT_vs_without/Dataset_nr_comparisons.tsv',sep='\t')
print('Done')
    