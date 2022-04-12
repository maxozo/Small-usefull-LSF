import os
from glob import glob
Directory = '/nfs/team151_data03/phase_impute_ref_panel/uk10k+1000g-phase3/impute2'
Out_dir = '/lustre/scratch123/hgi/projects/bhf_finemap/imputation/uk10k_1000g_phase3/vcfs'
# List all the vcf files in the directory.

all_vcfs = glob(f'{Directory}/*.hap.gz')

for vcf1 in all_vcfs:
    vcf_name = vcf1.split('/')[-1].split('.')[0]
    path = vcf1.split('/')
    path.pop()
    path1 = '/'.join(path)

    chr1 = vcf_name.split('.')[0]
    os.system(f"bsub -R'select[mem>40000] rusage[mem=40000]' -J chr{chr1} -n 5 -M 40000 -o {chr1}.o -e {chr1}.e -q normal bash run.sh {path1} {vcf_name} {Out_dir}")
print('Done')
