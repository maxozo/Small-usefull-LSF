import pandas as pd
from pysam import VariantFile
import glob
# import multiprocessing as mp
All_Datasets = pd.read_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/donor_panels_vcf_paths.tsv',sep='\t')
vcf_file = All_Datasets['vcf_file_path'][4]
cellsnp_vcf = '/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc/genome1K.phase3.SNP_AF5e2.chr1toX.hg38.vcf.gz'

count=0
data = {}

def get_field_info(rec):
    #     #CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO
    # 1	11008	rs575272151	C	G	100	PASS	AF=0.0880591
    # 1	11012	rs544419019	C	G	100	PASS	AF=0.0880591
    f2=''
    filt = list(rec.filter)
    for f1 in filt:
        f2+=f"{f1}"
    info_fields = list(rec.info)
    info_string=''
    for i_field in info_fields:
        info_string+=f"{i_field}={rec.info[i_field][0]};"    
    return {'#CHROM':rec.chrom,
                          'POS':rec.pos,
                          'ID':rec.id,
                          'REF':rec.alleles[0],
                          'ALT':rec.alleles[1],
                          'QUAL':rec.qual,
                          'FILTER':f2,
                          'INFO':info_string,
                          'identifier':f"{rec.chrom}---{rec.pos}"}
    

cellsnp_sites=[]
bcf_in = VariantFile(cellsnp_vcf) 
for rec in bcf_in.fetch():
    sites = get_field_info(rec)    
    cellsnp_sites.append(sites)
Dataset = pd.DataFrame(cellsnp_sites)    
pd.DataFrame(cellsnp_sites).to_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/analysis/mo11/cellsnp_sites_file_expanded/full_cellsnp_sites.tsv')

# All Sites in VCF files used
data_ukbb_elgh_cellsnp = []
for vcf_file in All_Datasets['vcf_file_path']:
    bcf_in = VariantFile(vcf_file) 
    for rec in bcf_in.fetch():
        sites = get_field_info(rec)    
        data_ukbb_elgh_cellsnp.append(sites)
pd.DataFrame(data_ukbb_elgh_cellsnp).to_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/analysis/mo11/cellsnp_sites_file_expanded/full_data_ukbb_elgh_cellsnp.tsv')
print('done with full_data_ukbb_elgh_cellsnp')

# ELGH sites
elgh_sites = []
elgh_full = '/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/filtered_genotypes/vcf/merged_bcf/GT_AF_ELGH_Concat.bcf.gz'
bcf_in = VariantFile(elgh_full) 
for rec in bcf_in.fetch():
    sites = get_field_info(rec)    
    elgh_sites.append(sites)
print('done with ELGH')
pd.DataFrame(elgh_sites).to_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/analysis/mo11/cellsnp_sites_file_expanded/full_elgh_sites_all.tsv')

# UKBB_sites = /lustre/scratch123/hgi/projects/ukbiobank_genotypes/FullRelease/Imputed/VCFs/hg38_bcf_sorted
all_vcfs = glob.glob(f'/lustre/scratch123/hgi/projects/ukbiobank_genotypes/FullRelease/Imputed/VCFs/hg38_bcf_sorted/*.bcf.gz')
ukbb_sites = []
for vcf_file in all_vcfs:
    print(vcf_file)
    count=0
    bcf_in = VariantFile(vcf_file) 
    for rec in bcf_in.fetch():
        sites = get_field_info(rec)    
        ukbb_sites.append(sites)
pd.DataFrame(ukbb_sites).to_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/analysis/mo11/cellsnp_sites_file_expanded/full_ukbb_all_sites.tsv')
print('done with full_ukbb_all_sites')

# UKBB_sites = /lustre/scratch123/hgi/projects/ukbiobank_genotypes/FullRelease/Imputed/VCFs/hg38_bcf_sorted
all_vcfs = glob.glob(f'/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/filtered_genotypes/vcf/*.vcf.gz')
elgh_not_merged_sites = []
for vcf_file in all_vcfs:
    print(vcf_file)
    count=0
    bcf_in = VariantFile(vcf_file) 
    for rec in bcf_in.fetch():
        sites = get_field_info(rec)    
        elgh_not_merged_sites.append(sites)
pd.DataFrame(ukbb_sites).to_csv('/lustre/scratch123/hgi/projects/ukbb_scrna/analysis/mo11/cellsnp_sites_file_expanded/full_elgh_not_merged_sites.tsv')
print('done with full_elgh_not_merged_sites')
