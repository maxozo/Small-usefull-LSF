import pandas as pd
import glob
import re
all_inputs = glob.glob("/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/fetch/*/results/yascp_inputs/input.tsv")
bridge = pd.read_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/secret/bridge.txt',sep='\t')
missing = []
for p1 in all_inputs:
    print(p1)
    Data = pd.read_csv(p1,sep='\t')
    for id1 in Data['donor_vcf_ids']:
        print(id1)
        pool=Data[Data['donor_vcf_ids']==id1]['experiment_id'].values[0]
        all_ids_expected = id1.replace("'","").split(',')
        for id3 in all_ids_expected:
            id_lookup = str(id3)
            id_lookup = re.sub(r"^0*", "",id_lookup)
            
            if any(bridge['s00046_id'].astype(str).str.contains(id_lookup)):
                _='in bridging file'
            else:
                if 'U937' in id_lookup:
                    continue
                elif 'THP1' in id_lookup:
                    continue
                else:
                    _='not in bridging file'
                    tranche = p1.split("/")[-4]
                    missing.append({'tranche':tranche,'pool':pool,'id':id_lookup})
        # now look up whether the ids are in the bridge files.
d2 = pd.DataFrame(missing) 
d2.to_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/secret/missing_vacutainer_to_oragene_id.tsv',sep='\t',index=False)      
set(d2['tranche']) 
len(set(d2['id']))
set(d2['pool']) 
print('Done')

