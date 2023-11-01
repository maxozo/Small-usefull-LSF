import pandas as pd
import re

Data = pd.read_csv('/lustre/scratch123/hgi/projects/macromap/eQTL_again/premapping.csv')
Data_kinship = pd.read_csv('/lustre/scratch123/hgi/projects/macromap/Analysis/LIMIX/kinship_matrix.tsv',sep='\t')

Data2=pd.DataFrame()
Data2['Genotype']=Data_kinship['Unnamed: 0']
Data2['RNA']=Data2['Genotype'].str.split('-').str[1]
# Data2 = pd.read_csv('/lustre/scratch123/hgi/projects/macromap/Analysis/LIMIX/sample_mapping.tsv',sep='\t')
Data['Genotype']=''
Data['RNA']=''


data_all = []
for donor2 in list(set(Data['Donor line'])):
    
    print(donor2)
    match = re.match(r"([a-z]+)([0-9]+)", donor2, re.I)
    items = match.groups()
    donor = '_'.join(items)
    Data.loc[Data['Donor line']==donor2,'RNA']=donor
    try:
        Genotype = Data2[Data2.RNA == donor].Genotype
        if len(Genotype)==0:
            Genotype = Data2[Data2.RNA == items[0]].Genotype
        # data_all.append({'Genotype':Genotype,'RNA':donor})
        Data.loc[Data['Donor line']==donor2,'Genotype']=Genotype.values[0]
        
    except:
        print(f'missing {donor}')
        data_all.append(donor)
missing = pd.DataFrame(set(Data['RNA'])-set(Data2.RNA))
Data = Data[Data['Genotype']!='']
df = pd.DataFrame({'Genotype':Data['Genotype'],'RNA':Data['Sanger Sample ID']})
df.to_csv('/lustre/scratch123/hgi/projects/macromap/Analysis/LIMIX/sample_mapping.tsv',index=False,sep='\t')
print('finished')