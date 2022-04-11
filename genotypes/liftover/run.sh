vcf=$1
name=$2
out_path=$3
echo $name
echo $out_path
genomeref="/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/genome.fa"
zcat $vcf > $out_path/vcf2.vcf
CrossMap.py vcf /lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/GRCh37_to_GRCh38.chain.gz $out_path/vcf2.vcf $genomeref $out_path/hg38_$2.vcf
bgzip -c $out_path/hg38_$2.vcf > $out_path/hg38_$2.vcf.gz

# bcftools annotate -x INFO,^FORMAT/GT,FORMAT/AF $1 -Oz --threads 5 -o $2
