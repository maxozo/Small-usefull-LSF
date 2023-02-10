for cc in {1..22}
do
plink2 --bfile ../Feb28k_autosome_maf0.01_geno0.01_excPalindromic_SNPonly_updated \
 --recode vcf --real-ref-alleles --chr "$cc" \
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


# for cc in {1..22}
# do
# plink2 --bfile ../Feb28k_autosome_maf0.01_geno0.01_excPalindromic_SNPonly_updated \
#  --recode vcf --real-ref-alleles --chr "$cc" \
# --out Feb28k_1000samples_chr"$cc" --memory 2000 
# # # Chromosomes are encoded with prefix "chr" for build 38
# # head -n 6 Feb28k_1000samples_chr"$cc".vcf > temp_chr"$cc".vcf.header
# # cat Feb28k_1000samples_chr1.vcf|tail -n +7 |awk '{print"chr"$0}' > temp_chr1.vcf
# # cat temp_chr"$cc".vcf.header temp_chr"$cc".vcf > Feb28k_1000samples_chr"$cc".vcf
# bcftools view Feb28k_1000samples_chr"$cc".vcf -Oz -o Feb28k_1000samples_chr"$cc".vcf.gz
# bcftools index --threads 5 Feb28k_1000samples_chr"$cc".vcf.gz
# bcftools sort Feb28k_1000samples_chr"$cc".vcf.gz -Oz -o sorted_Feb28k_1000samples_chr"$cc".vcf.gz
# bcftools index --threads 5 sorted_Feb28k_1000samples_chr"$cc".vcf.gz
# done


# for group in 1 2 
# do

# for cc in {1..22}
# do
# plink --bfile Feb28k_autosome_maf0.01_geno0.01_hwe6Bangladeshi_excPalindromic_SNPonly_updated \
# --keep random_group"$group"_keep.txt --recode vcf --real-ref-alleles --chr "$cc" \
# --out Feb28k_updated_group"$group"_chr"$cc" --memory 2000 
# # Chromosomes are encoded with prefix "chr" 
# head -n 6 Feb28k_updated_group"$group"_chr"$cc".vcf > temp_group"$group"_chr"$cc".vcf.header
# cat Feb28k_updated_group"$group"_chr"$cc".vcf|tail -n +7 |awk '{print"chr"$0}' > temp_group"$group"_chr"$cc".vcf
# cat temp_group"$group"_chr"$cc".vcf.header temp_group"$group"_chr"$cc".vcf > Feb28k_updated_group"$group"_chr"$cc"_chrencoded.vcf
# vcf-sort Feb28k_updated_group"$group"_chr"$cc"_chrencoded.vcf | bgzip -c > Feb28k_updated_group"$group"_chr"$cc"_chrencoded.vcf.gz
# # clean up
# rm *.nosex temp_group"$group"_chr"$cc".vcf* Feb28k_updated_group"$group"_chr"$cc".vcf
# done

# done