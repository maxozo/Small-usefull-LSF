vcf1=$1
name=$2
out_dir=$3
tmp="/lustre/scratch123/hgi/projects/ukbiobank_genotypes/FullRelease/Imputed/VCFs/tmp3/$2"
# bcftools view -h $vcf1 > header_$name.txt
# bcftools reheader -h  header_$name.txt -o $out_dir/rehead_$name.vcf.gz $vcf1 
# bcftools sort $out_dir/rehead_$name.vcf.gz -Oz -o $out_dir/sorted$name.vcf.gz
# bcftools index --threads 10 $out_dir/sorted$name.vcf.gz
# (zcat /lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/1000G_full_GRCh38_sorted_chrAdded.vcf.gz | grep ^\#; zcat /lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/1000G_full_GRCh38_sorted_chrAdded.vcf.gz | grep -v ^\# | sort -k1,1d -k2,2n) | bgzip --threads 5 -c > sorted_name.bcf.gz
plink2 --vcf /lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/1000G_full_GRCh38_sorted_chrAdded.vcf.gz --sort-vars --export vcf 'bgz' --out /lustre/scratch123/hgi/projects/ukbiobank_genotypes/FullRelease/Imputed/VCFs/tmp3/test_sort 
# bcftools sort -m 70G --temp-dir $tmp $vcf1 -Ou -o $out_dir/sorted_$name.bcf
# bgzip --threads 5 $out_dir/sorted_$name.bcf
# bcftools index --threads 5 $out_dir/sorted_$name.bcf.gz