bgen=$1
name=$2

out_path='/lustre/scratch123/hgi/teams/hgi/mo11/tmp/ukbb/hg38'
out_path37='/lustre/scratch123/hgi/teams/hgi/mo11/tmp/ukbb/hg37'
sample='/lustre/scratch123/hgi/projects/ukbb_scrna/ukb_genetics_download/ukb22828_c1_b0_v3_s487202.sample'
genomeref="/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/liftover_chain_files/genome.fa"
echo $bgen
plink2 --bgen $bgen ref-last --sample $sample --export vcf vcf-dosage=DS --out $out_path37/ref_last_$name
# CrossMap.py vcf /lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/liftover_chain_files/GRCh37_to_GRCh38.chain.gz $out_path37/$name.vcf $genomeref $out_path/hg38_$name.vcf
# bgzip -c $out_path/hg38_$name.vcf > $out_path/hg38_$name.vcf.gz

# bsub -R'select[mem>70000] rusage[mem=70000]' -J chr1 -n 10 -M 70000 -o chr1.o -e chr1.e -q normal CrossMap.py vcf /lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/liftover_chain_files/GRCh37_to_GRCh38.chain.gz /lustre/scratch123/hgi/teams/hgi/mo11/tmp/ukbb/hg37/ukb_imp_chr2_v3.vcf /lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/liftover_chain_files/genome.fa /lustre/scratch123/hgi/teams/hgi/mo11/tmp/ukbb/backup/hg38_ukb_imp_chr2_v3.vcf
# bcftools annotate -x INFO,^FORMAT/GT,FORMAT/AF $1 -Oz --threads 5 -o $2
# CrossMap.py vcf /lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/liftover_chain_files/GRCh37_to_GRCh38.chain.gz /lustre/scratch123/hgi/projects/bhf_finemap/random/genotypes/just_positions/test.vcf /lustre/scratch123/hgi/teams/hgi/mo11/tmp/Homo_sapiens.GRCh38.dna.primary_assembly.fa hg38_try.vcf
