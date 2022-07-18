path='/lustre/scratch123/hgi/projects/ukbiobank_genotypes/FullRelease/Imputed/VCFs/hg38_bcf_sorted'
outpath='/lustre/scratch123/hgi/projects/ukbiobank_genotypes/FullRelease/Imputed/VCFs/CellSNP_subset_hg38'
name=$1
chr=$2
cat /lustre/scratch123/hgi/projects/bhf_finemap/random/genotypes/cellsnp_sites/CellSNP_subset2.tsv | grep "19 " > chr$chr.tsv
cat /lustre/scratch123/hgi/projects/bhf_finemap/random/genotypes/cellsnp_sites/CellSNP_subset2.tsv | grep "^$chr\s" > chr$chr.tsv
echo "bcftools view $path/$name.bcf.gz --regions-file /lustre/scratch123/hgi/projects/bhf_finemap/random/genotypes/cellsnp_sites/test.tsv -Ob -o $outpath/sub_$name.bcf.gz"
bcftools view $path/$name.bcf.gz --threads 5 --regions-file "chr$chr.tsv" -Ob -o $outpath/sub_$name.bcf.gz