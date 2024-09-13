import glob
import os
import pandas as pd
# Cardinal_46226_Nov_29_2022
#  Here we triger the GT match script for all the samples using the corect bridging file.
all_pools = glob.glob('/lustre/scratch123/hgi/projects/cardinal_analysis/freezes/freeze0/qc/*/infered_genotypes/*/')
all_pools_todo = pd.DataFrame(all_pools,columns=['col1'])
all_pools_todo = set(all_pools_todo['col1'].str.split('/').str[-2])
count=0
count2=0
# only perform this operation in pools where there is no gt_match_FullGT_Jul2024_final folder
all_pools_performed = pd.DataFrame(glob.glob('/lustre/scratch123/hgi/projects/cardinal_analysis/freezes/freeze0/qc/*/infered_genotypes/*/gt_match_FullGT_Jul2024_final'),columns=['col1'])
all_pools_performed = set(all_pools_performed['col1'].str.split('/').str[-2])

all_pools_todo = all_pools_todo-all_pools_performed
for p1 in all_pools:
    count2+=1
    p1=p1[:-1]
    pool = p1.split('/')[-1]
    if pool not in all_pools_todo:
        continue
    else:
        print(f'analysing {p1}')
    # we loop through each of the pools and link the correct input files.
    # then we cd to that directory and triger the nextflow script to perform the gt check.
    try:
        os.mkdir(f'{p1}/gt_match_FullGT_Jul2024')
    except:
        _ ='exists'
    try:
        
        if pool=='CRD_CMB13076387':
            continue
        try:
            data = pd.read_csv(f"{p1}/gt_match_FullGT_Jul2024/gt.o",sep='xxxxx', names=['col'], engine='python')
            if len(data[data['col'].str.contains('Successfully')]) == 0:
                print(p1)
                print(count2)
                os.system(f'export NXF_SINGULARITY_CACHEDIR="/software/hgi/containers/yascp" && export SINGULARITY_DISABLE_CACHE=0 && chgrp -R hgi {p1}/gt_match_FullGT_Jul2024 && cd {p1}/gt_match_FullGT_Jul2024 ./ && export FILE="{pool}" && bash run.sh')
                count+=1
                if count>56:
                    break
        except:
            print(p1)
            print(count2)
            os.system(f'export NXF_SINGULARITY_CACHEDIR="/software/hgi/containers/yascp" && export SINGULARITY_DISABLE_CACHE=0 && chgrp -R hgi {p1}/gt_match_FullGT_Jul2024 && cd {p1}/gt_match_FullGT_Jul2024 && ln -s /lustre/scratch123/hgi/projects/cardinal_analysis/analysis/mo11/random/scRNA/rerun_gt_match_f0/input.nf ./ && ln -s /lustre/scratch123/hgi/projects/cardinal_analysis/analysis/mo11/random/scRNA/rerun_gt_match_f0/run.sh ./ && export FILE="{pool}" && bash run.sh')
            count+=1
            if count>56:
                break
    except:
        print('Already done')
print('Done')