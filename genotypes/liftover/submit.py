import os
from glob import glob
Directory = '/lustre/scratch119/humgen/projects/elgh_gsa/process_ELGH_genotype_data/Jul2021_44k/Imputed_TOPMed/vcf_from_QMUL'
Out_dir = '/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/filtered_genotypes/vcf'
# List all the vcf files in the directory.

all_vcfs = glob(f'{Directory}/*.vcf.gz')

for vcf1 in all_vcfs:
    vcf_name = vcf1.split('/')[-1]
    chr1 = vcf_name.split('.')[0]
    os.system(f"bsub -R'select[mem>40000] rusage[mem=40000]' -J {chr1} -n 5 -M 40000 -o {chr1}.o -e {chr1}.e -q normal bash run.sh {vcf1} {Out_dir}/GT_AF_{vcf_name}")
print('Done')
