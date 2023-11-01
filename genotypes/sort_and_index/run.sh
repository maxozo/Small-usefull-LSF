vcf1=$1
name=$2
out_dir=$3
tmp="/lustre/scratch123/hgi/projects/ukbiobank_genotypes/FullRelease/Imputed/VCFs/tmp3/$2"
# bcftools view -h $vcf1 > header_$name.txt
# bcftools reheader -h  header_$name.txt -o $out_dir/rehead_$name.vcf.gz $vcf1 
# bcftools sort $out_dir/rehead_$name.vcf.gz -Oz -o $out_dir/sorted$name.vcf.gz
# bcftools index --threads 10 $out_dir/sorted$name.vcf.gz
# bgzip --threads 10 $out_path/hg38_$name.vcf
bcftools sort -m 70G --temp-dir $tmp $vcf1 -Ob -o $out_dir/sorted_$name.bcf.gz
# bgzip --threads 5 $out_dir/sorted_$name.bcf
bcftools index --threads 5 $out_dir/sorted_$name.bcf.gz