vcf1=$1
name=$2
out_dir=$3
tmp="/lustre/scratch123/hgi/projects/ukbiobank_genotypes/FullRelease/Imputed/VCFs/tmp3/$2"
# bcftools view -h $vcf1 > header_$name.txt
# bcftools reheader -h  header_$name.txt -o $out_dir/rehead_$name.vcf.gz $vcf1 
# bcftools sort $out_dir/rehead_$name.vcf.gz -Oz -o $out_dir/sorted$name.vcf.gz
# bcftools index --threads 10 $out_dir/sorted$name.vcf.gz
(zcat /lustre/scratch123/hgi/projects/ukbiobank_genotypes/FullRelease/Imputed/VCFs/hg38/hg38_ukb_imp_chr2_v3.vcf.gz | grep ^\#; zcat /lustre/scratch123/hgi/projects/ukbiobank_genotypes/FullRelease/Imputed/VCFs/hg38/hg38_ukb_imp_chr2_v3.vcf.gz | grep -v ^\# | sort -k1,1d -k2,2n) | bgzip --threads 5 -c > /lustre/scratch123/hgi/projects/ukbiobank_genotypes/FullRelease/Imputed/VCFs/tmp3/test_sort/sorted_sorted_hg38_ukb_imp_chr2_v3.vcf.gz
# bcftools sort -m 70G --temp-dir $tmp $vcf1 -Ou -o $out_dir/sorted_$name.bcf
# bgzip --threads 5 $out_dir/sorted_$name.bcf
# bcftools index --threads 5 $out_dir/sorted_$name.bcf.gz