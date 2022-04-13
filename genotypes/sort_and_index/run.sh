vcf1=$1
name=$2
out_dir=$3

bcftools sort --threads 5 $vcf1 -Oz -o $out_dir/sorted$name.vcf.gz
bcftools index --threads 5 $out_dir/sorted$name.vcf.gz