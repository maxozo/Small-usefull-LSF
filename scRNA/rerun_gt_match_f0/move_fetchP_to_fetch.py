import glob
import os
import shlex
all_dirs_affected = glob.glob('/lustre/scratch123/hgi/projects/cardinal_analysis/freezes/freeze0/qc/*/infered_genotypes/*')

# for d1 in all_dirs_affected:
#     print(d1)
#     to_dir = '/'.join(d1.split('/')[:-1])+'/Fetch'
#     d2 = d1.replace(' ', "/\ ")

#     # Use shlex.quote to safely quote the directory names
#     quoted_d2 = shlex.quote(d1)
#     os.system(f"mv {quoted_d2} {to_dir}")

for d1 in all_dirs_affected:
    try:
        print(d1)
        pool = d1.split('/')[-1]
        # pool = d1.split('html_')[-1].split('.')[0]
        # p1 = d1.split('Summary_plots')[0]
        os.system(f"cd {d1}/gt_match_FullGT_Jul2024_final/{pool} && /software/hgi/pipelines/yascp_versions/yascp_v1.7/bin/enhance_stats.py -id {pool} -dm stats_{pool}_gt_donor_assignments.csv --genotype_phenotype_mapping /lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/secret/bridge_06_03_2024.tsv --input_file ../../../../Summary_plots/Fetch/Input/input_table.tsv -m false")
    except:
        print('miss')
    # os.system(f"cd {p1}infered_genotypes/{pool}/gt_match_FullGT_Jul2024/results/gtmatch/{pool} && enhance_stats.py -id {pool} -dm stats_{pool}_gt_donor_assignments.csv --genotype_phenotype_mapping /lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/secret/bridge_06_03_2024.tsv --input_file '../../../../../../Summary_plots/Fetch\ Pipeline/Input/input_table.tsv' -m false")
# ls /lustre/scratch123/hgi/projects/cardinal_analysis/freezes/freeze0/qc/Cardinal_46499_Jan_21_2023/Summary_plots/Fetch\ Pipeline
# "pd enhance_stats.py -id {pool} -dm stats_{pool}_gt_donor_assignments.csv --genotype_phenotype_mapping /lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/secret/bridge_06_03_2024.tsv --input_file '../../../../../../Summary_plots/FetchInput/input_table.tsv' -m false"
print('1')