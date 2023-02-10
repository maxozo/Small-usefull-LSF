for cc in {1..22}
do
plink2 --bfile ../../Feb28k_autosome_maf0.01_geno0.01_excPalindromic_SNPonly \
--keep keep_1000_samples.txt --recode vcf --real-ref-alleles --chr "$cc" \
--out Feb28k_1000samples_chr"$cc" --memory 2000 
# # Chromosomes are encoded with prefix "chr" for build 38
head -n 6 Feb28k_1000samples_chr"$cc".vcf > temp_chr"$cc".vcf.header
sed -i "s/ID=$cc/ID=chr$cc/g" temp_chr"$cc".vcf.header
cat Feb28k_1000samples_chr"$cc".vcf|tail -n +7 |awk '{print"chr"$0}' > temp_chr"$cc".vcf
cat temp_chr"$cc".vcf.header temp_chr"$cc".vcf > Feb28k_1000samples_chr"$cc".vcf
bcftools view Feb28k_1000samples_chr"$cc".vcf -Oz -o Feb28k_1000samples_chr"$cc".vcf.gz
bcftools index --threads 5 Feb28k_1000samples_chr"$cc".vcf.gz
bcftools sort Feb28k_1000samples_chr"$cc".vcf.gz -Oz -o sorted_Feb28k_1000samples_chr"$cc".vcf.gz
bcftools index --threads 5 sorted_Feb28k_1000samples_chr"$cc".vcf.gz
done