import os
from glob import glob
Directory = '/lustre/scratch123/hgi/projects/ukbiobank_genotypes/FullRelease/Imputed/EGAD00010001474'

# List all the vcf files in the directory.
Sample = '/lustre/scratch123/hgi/projects/ukbb_scrna/ukb_genetics_download/ukb22828_c1_b0_v3_s487202.sample'
all_vcfs = glob(f'{Directory}/*.bgen')

for vcf1 in all_vcfs:
    vcf_name = vcf1.split('/')[-1].split('.')[0]
    chr1 = vcf_name
    if (chr1=='ukb_imp_chr22_v3'):
    # if (chr1=='ukb_imp_chr9_v3' or chr1=='ukb_imp_chr11_v3' or chr1=='ukb_imp_chr13_v3'):
        os.system(f"bsub -R'select[mem>60000] rusage[mem=60000]' -J ref_first_run{chr1} -n 10 -M 60000 -o {chr1}.o -e {chr1}.e -q long bash ref_first_run.sh {vcf1} {vcf_name}")
        # os.system(f"bsub -R'select[mem>70000] rusage[mem=70000]' -J ref_last_run{chr1} -n 10 -M 70000 -o {chr1}.o -e {chr1}.e -q normal bash ref_last_run.sh {vcf1} {vcf_name}")

    # chr1="ukb_imp_chr21_v3"
    # vcf_name="/lustre/scratch123/hgi/projects/ukbiobank_genotypes/FullRelease/Imputed/EGAD00010001474/ukb_imp_chr21_v3.bgen"
#     os.system(f"bsub -R'select[mem>70000] rusage[mem=70000]' -J {chr1} -n 10 -M 70000 -o {chr1}.o -e {chr1}.e -q normal bash run.sh {vcf1} {vcf_name}")
print('Done')
