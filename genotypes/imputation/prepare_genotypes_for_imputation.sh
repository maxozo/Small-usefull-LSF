#!/bin/bash


## echo 'bash ~/projects/covid19-vo-study/scripts/prepare_genotypes_for_imputation.sh' | bsub -n2 -R"span[hosts=1]" -o /lustre/scratch123/hgi/projects/covid_vo_study/analysis/log_files/prepare_genotypes_for_imputation.out -R "select[mem>=20000] rusage[mem=20000]" -M20000


##### Download HRC sites file

# https://www.well.ox.ac.uk/~wrayner/tools/
# ftp://ngs.sanger.ac.uk/production/hrc/HRC.r1-1/HRC.r1-1.GRCh37.wgs.mac5.sites.tab.gz
# /lustre/scratch123/hgi/projects/covid_vo_study/analysis/imputation/HRC.r1-1.GRCh37.wgs.mac5.sites.tab.gz


##### Calculate AF #####

# INFILE=/lustre/scratch123/hgi/projects/covid_vo_study/data/GSP_2020-276-ILL_GSAHTM_N-2418/GSP_2020-276-ILL_GSAHTM_N-2418_QC 
# OUTFILE=/lustre/scratch123/hgi/projects/covid_vo_study/analysis/variantQC/GSP_2020-276-ILL_GSAHTM_N-2418_QC
# plink --bfile $INFILE --freq --out $OUTFILE


##### Check alleles and generate Run-plink.sh script which needs to be modified #####

# BIM=/lustre/scratch123/hgi/projects/covid_vo_study/data/GSP_2020-276-ILL_GSAHTM_N-2418/GSP_2020-276-ILL_GSAHTM_N-2418_QC.bim
# AF=/lustre/scratch123/hgi/projects/covid_vo_study/analysis/variantQC/GSP_2020-276-ILL_GSAHTM_N-2418_QC.frq
# REF=/lustre/scratch123/hgi/projects/covid_vo_study/analysis/imputation/HRC.r1-1.GRCh37.wgs.mac5.sites.tab 
# OUTFILE=/lustre/scratch123/hgi/projects/covid_vo_study/analysis/imputation/GSP_2020-276-ILL_GSAHTM_N-2418_QC

# perl ~/projects/covid19-vo-study/imputation/HRC-1000G-check-bim-NoReadKey.pl -b $BIM -f $AF -r $REF -h -o $OUTFILE


##### Run Run-plink.sh #####

## echo 'bash /lustre/scratch123/hgi/projects/covid_vo_study/analysis/imputation/GSP_2020-276-ILL_GSAHTM_N-2418_QC/Run-plink.sh' | bsub -n2 -R"span[hosts=1]" -o /lustre/scratch123/hgi/projects/covid_vo_study/analysis/log_files/Run-plink.out -R "select[mem>=20000] rusage[mem=20000]" -M20000                                                           


##### Get sites to check chromosome name and whether sorted by position #####

# INFILE=/lustre/scratch123/hgi/projects/covid_vo_study/analysis/imputation/GSP_2020-276-ILL_GSAHTM_N-2418_QC/GSP_2020-276-ILL_GSAHTM_N-2418_QC-updated.vcf.gz
# OUTFILE=/lustre/scratch123/hgi/projects/covid_vo_study/analysis/imputation/GSP_2020-276-ILL_GSAHTM_N-2418_QC/GSP_2020-276-ILL_GSAHTM_N-2418_QC-updated.sites.vcf.gz

# zcat $INFILE | cut -f1-8 | gzip > $OUTFILE


##### Rename chr23 to chrX #####

## cp /lustre/scratch123/hgi/projects/mpn_prs/scratch115/jg30/dat/plink2ensembl-chr23.txt  /lustre/scratch123/hgi/projects/covid_vo_study/analysis/imputation/GSP_2020-276-ILL_GSAHTM_N-2418_QC/

# INFILE=/lustre/scratch123/hgi/projects/covid_vo_study/analysis/imputation/GSP_2020-276-ILL_GSAHTM_N-2418_QC/GSP_2020-276-ILL_GSAHTM_N-2418_QC-updated.vcf.gz
# OUTFILE=/lustre/scratch123/hgi/projects/covid_vo_study/analysis/imputation/GSP_2020-276-ILL_GSAHTM_N-2418_QC/GSP_2020-276-ILL_GSAHTM_N-2418_QC_chr1-X.vcf.gz
# CHROM=/lustre/scratch123/hgi/projects/covid_vo_study/analysis/imputation/GSP_2020-276-ILL_GSAHTM_N-2418_QC/plink2ensembl-chr23.txt 

# bcftools annotate -Oz --rename-chrs $CHROM $INFILE > $OUTFILE


##### Final check - use python2 #####

## The resulting VCF file also needs to be checked for compatibility
## with the input required by the Sanger server.
## To do this, download the checkVCF tool from
## http://qbrc.swmed.edu/zhanxw/software/checkVCF/checkVCF-20140116.tar.gz
## This tarball includes the checkVCF.py script, the reference genome
## (hs37d5.fa) in FASTA format and its index file (hs37d5.fa.fai).
## wget http://qbrc.swmed.edu/zhanxw/software/checkVCF/checkVCF-20140116.tar.gz
## gunzip checkVCF-20140116.tar.gz
## tar -xvf checkVCF-20140116.tar

## cp /lustre/scratch123/hgi/projects/mpn_prs/scratch115/jg30/dat/README.md /lustre/scratch123/hgi/projects/covid_vo_study/analysis/imputation/GSP_2020-276-ILL_GSAHTM_N-2418_QC/
## cp /lustre/scratch123/hgi/projects/mpn_prs/scratch115/jg30/dat/checkVCF.py /lustre/scratch123/hgi/projects/covid_vo_study/analysis/imputation/GSP_2020-276-ILL_GSAHTM_N-2418_QC/

cd /lustre/scratch123/hgi/projects/covid_vo_study/analysis/imputation/GSP_2020-276-ILL_GSAHTM_N-2418_QC
GRC37=/lustre/scratch123/hgi/projects/mpn_prs/scratch115/jg30/dat/hs37d5.fa
INFILE=/lustre/scratch123/hgi/projects/covid_vo_study/analysis/imputation/GSP_2020-276-ILL_GSAHTM_N-2418_QC/GSP_2020-276-ILL_GSAHTM_N-2418_QC_chr1-X.vcf.gz
OUTFILE=/lustre/scratch123/hgi/projects/covid_vo_study/analysis/imputation/GSP_2020-276-ILL_GSAHTM_N-2418_QC/GSP_2020-276-ILL_GSAHTM_N-2418_QC_chr1-X

/software/python-2.7.16/bin/python checkVCF.py -r $GRC37 -o $OUTFILE $INFILE


##### Imputation with Sanger server #####

# https://imputation.sanger.ac.uk

### Prepare your data ###
# Valid VCF
# All alleles on the forward strand
# Coordinates are on GRCh37
# REF allele matches GRCh37. See the resources for help checking and fixing the REF allele.
# A single VCF file, not one file per-chromosome
# Records are sorted by genomic position (chromosomal order is not important)
# Chromosome names should be 1, 2, 3, etc… not chr1, chr2, chr3, etc… They should match the names in this reference index file. 
# Some programs will represent X as 23, Y as 24, etc…. Please remove or replace these names. See the resources for help renaming chromosomes in a VCF.
# If not requesting pre-phasing, then all sites and samples should be phased with no missing data.

# Run ID: 1c57695e0275315aa048645a291a1128
# Label: Covid19-Vo-Italy
# Status: new
# Panel: Haplotype Reference Consortium (r1.1)
# Pipeline: EAGLE2+PBWT
# https://imputation.sanger.ac.uk/?status=1&rid=1c57695e0275315aa048645a291a1128

### Globus ID ###
# kw8@globusid.org
# Ro*L*!
bcftools convert --hapsample2vcf /lustre/scratch123/hgi/projects/bhf_finemap/imputation/uk10k_1000g_phase3/Done_21_all_4.hap_altered.hap,/nfs/team151_data03/phase_impute_ref_panel/uk10k+1000g-phase3/impute2/21.samples
bcftools convert --hapsample2vcf /lustre/scratch123/hgi/projects/bhf_finemap/imputation/uk10k_1000g_phase3/Done_21_all_4.hap_altered.hap,/nfs/team151_data03/phase_impute_ref_panel/uk10k+1000g-phase3/impute2/21.samples --threads 5 -Oz -o 21_uk10k_1000g_phase3.vcf.gz

bcftools convert --haplegendsample2vcf 21.hap.gz,21.legend.gz,21.samples --threads 5 -Oz -o 21_uk10k_1000g_phase3.vcf.gz


paste -d' ' <(yes 21) <(zcat 21.legend.gz | tail -n +2) <(zcat 21.hap.gz) > 21_all_4.hap
paste -d' ' <(zcat 21.legend.gz | tail -n +2) <(zcat 21.hap.gz) > 21_all_4.hap
paste -d' ' <(yes 21) <(cat 21_all_4.hap) > 21_all_4_21.hap
nohup perl -lne 'print "21 $_"' 21_all_4.hap >21_all_4.hap_altered.hap
sed -i -e 's/^/21 /' 21_all_3.hap

### Link to an endpoint with your data ###
# For Sanger users: The Sanger Institute has a site licence for Globus,
# so Sanger users can enter sangerinstitute#farm in the right-hand panel
# and then authenticate using their Sanger credentials. This will enable
# access to any files mounted on the Sanger Insitute farm.

### Confirm data upload ###
# Wait for email

### Download data ###
## Wait for email and follow instructions

### Imputed data ###
/lustre/scratch123/hgi/projects/covid_vo_study/analysis/imputation/GSP_2020-276-ILL_GSAHTM_N-2418_QC_imputed/


# Eagle restricts analysis to sites that are contained in both the
# target and reference (with matching CHR, POS, and ALT fields) and are
# biallelic in the target VCF/BCF. Sites for which the REF and ALT
# alleles are swapped in the target VCF/BCF relative to the reference
# are dropped by default. This requirement can be relaxed via the
# --allowRefAltSwap flag, which causes REF/ALT swaps to be tolerated
# (and automatically flipped) for true SNPs. For indels, REF/ALT swaps
# are always dropped due to the possibility of different indels
# appearing to be the same. (Thanks to Giulio Genovese for pointing out
# this subtlety.)
