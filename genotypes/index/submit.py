import os
from glob import glob
Directory = '/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/filtered_genotypes/vcf'
Out_dir = '/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/filtered_genotypes/vcf'
# List all the vcf files in the directory.

all_vcfs = glob(f'{Directory}/*.vcf.gz')

for vcf1 in all_vcfs:
    vcf_name = vcf1.split('/')[-1]
    chr1 = vcf_name.split('.')[0]
    os.system(f"bsub -R'select[mem>20000] rusage[mem=20000]' -J {chr1} -n 3 -M 20000 -o {chr1}.o -e {chr1}.e -q normal \
        bash run.sh {vcf1}")
print('Done')
