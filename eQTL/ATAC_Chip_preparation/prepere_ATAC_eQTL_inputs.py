import pandas as pd
import re
## Output data needs to be in the folowing format:
# Genotype	RNA	Sample_Category
# 103_S456	UVE_ATC13036550	general
# 127_S461	UVE_ATC13036551	general
# 152_S482	UVE_ATC13036552	general
# 168_S484	UVE_ATC13036553	general

# # Sample input:
# Genotype	RNA	Sample_Category
# HPSI0713i-aehn_22	MM_oxLDL9752083	M0_0
# HPSI0713i-aehn_22	MM_oxLDL9752084	M0_100
# HPSI0713i-aehn_22	MM_oxLDL9752085	M1_0

ATAC_Input_FILE_Used = pd.read_csv('/lustre/scratch123/hgi/projects/macromap/ATAC/results/inputs/Macromap_ATAC_Input.csv')
Metadata_File = pd.read_csv('/lustre/scratch123/hgi/projects/macromap/ATAC/results/inputs/Maria_oxLDL project metadata - ATAC Sequencing samples.csv')
All_Genotypes = pd.read_csv('/lustre/scratch123/hgi/projects/macromap/ATAC/eQTLs/all_hipsci_samples.tsv',header=None,names=['Genotype'])
All_Genotypes['RNA']=All_Genotypes['Genotype'].str.split('-').str[1]
All_Data = []
count=0
for i,row1 in ATAC_Input_FILE_Used.iterrows():
    print(i)
    count+=1
    RNA = f"{row1.group}_R{row1.replicate}"
    Sample_Category=row1.group
    Sample_ID = row1.fastq_1.split('/')[-2]
    Donor_line = Metadata_File[Metadata_File['SAMPLEID']==Sample_ID]['LINE'].values[0]
    Sample_Category = Metadata_File[Metadata_File['SAMPLEID']==Sample_ID]['SAMPLETYPE'].values[0]
    Genotype_id = All_Genotypes['Genotype']
    match = re.match(r"([a-z]+)([0-9]+)", Donor_line, re.I)
    items = match.groups()
    donor = '_'.join(items)
    print(donor)
    
    try:
        Genotype = All_Genotypes[All_Genotypes.RNA == donor].Genotype
        if len(Genotype)==0:
            Genotype = All_Genotypes[All_Genotypes.RNA == items[0]].Genotype
        All_Data.append({'Genotype':Genotype.values[0],'RNA':RNA,'Sample_Category':Sample_Category})
    except:
        print(f'missing {donor}')
        Genotype = ''
    
final_df = pd.DataFrame(All_Data)
final_df.to_csv('/lustre/scratch123/hgi/projects/macromap/ATAC/eQTLs/sample_mappings2.tsv',index=False,sep='\t')
print('Done')