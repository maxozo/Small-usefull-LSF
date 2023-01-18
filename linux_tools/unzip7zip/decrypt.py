import os
import pandas as pd
import glob
# before merging we need to decrypt the genotype_bridge files using:
# 
p='pasword'
Directory = '/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/ukb_bridge_files/encrypted'
all_files = glob.glob(f'{Directory}/genotyping_bridge_*.7z')
All_Data = pd.DataFrame()
Decrypt_dir = '/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/ukb_bridge_files/genotype_bridge'
for bf1 in all_files:
    # print(bf1)
    Name = bf1.split('/')[-1].split('.')[0]
    if(os.path.exists(f'{Decrypt_dir}/{Name}.csv')):
        print(('Yes Done'))
    else:
        print(('No Done'))
        print(bf1)
        os.system(f'cd {Decrypt_dir} && 7z x {bf1} -p"{p}"')


Directory = '/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/ukb_bridge_files/encrypted'
all_files = glob.glob(f'{Directory}/shipping_manifest_*.7z')
All_Data = pd.DataFrame()
Decrypt_dir = '/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/ukb_bridge_files/shipping_manifest'
for bf1 in all_files:
    # print(bf1)
    Name = bf1.split('/')[-1].split('.')[0]
    if(os.path.exists(f'{Decrypt_dir}/{Name}.csv')):
        print(('Yes Done'))
    else:
        print(('No Done'))
        print(bf1)
        os.system(f'cd {Decrypt_dir} && 7z x {bf1} -p"{p}"')
