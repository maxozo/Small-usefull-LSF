# echo "1 chr1" >> chr_name_conv.txt
# echo "2 chr2" >> chr_name_conv.txt
# echo "3 chr3" >> chr_name_conv.txt
# echo "4 chr4" >> chr_name_conv.txt
# echo "5 chr5" >> chr_name_conv.txt
# echo "6 chr6" >> chr_name_conv.txt
# echo "7 chr7" >> chr_name_conv.txt
# echo "8 chr8" >> chr_name_conv.txt
# echo "9 chr9" >> chr_name_conv.txt
# echo "10 chr10" >> chr_name_conv.txt
# echo "11 chr11" >> chr_name_conv.txt
# echo "12 chr12" >> chr_name_conv.txt
# echo "13 chr13" >> chr_name_conv.txt
# echo "14 chr14" >> chr_name_conv.txt
# echo "15 chr15" >> chr_name_conv.txt
# echo "16 chr16" >> chr_name_conv.txt
# echo "17 chr17" >> chr_name_conv.txt
# echo "18 chr18" >> chr_name_conv.txt
# echo "19 chr19" >> chr_name_conv.txt
# echo "20 chr20" >> chr_name_conv.txt
# echo "21 chr21" >> chr_name_conv.txt
# echo "22 chr22" >> chr_name_conv.txt
vcf_in=$1
vcf_name=${vcf_in##*/}
dirname_path=$(dirname $vcf_in)
bcftools annotate --rename-chrs /lustre/scratch123/hgi/projects/cardinal_analysis/analysis/mo11/random/genotypes/add_chr_prefix/chr_name_conv.txt \
    $vcf_in \
         -Oz -o $dirname_path/chr_pr__$vcf_name
bcftools index $dirname_path/chr_pr__$vcf_name