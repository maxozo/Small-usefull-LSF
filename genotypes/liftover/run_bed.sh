vcf=$1
name=$2
out_path=$3
genomeref="/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/genome.fa"
CrossMap.py bed /lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/liftover_chain_files/GRCh37_to_GRCh38.chain.gz $vcf $out_path/hg38_$2.bed
# bgzip -c $out_path/hg38_$2.bed > $out_path/hg38_$2.bed.gz