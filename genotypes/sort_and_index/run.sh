vcf1=$1
name=$2
out_dir=$3

bcftools sort $vcf1 -Oz -o $out_dir/sorted$name.vcf.gz
bcftools index $out_dir/sorted$name.vcf.gz