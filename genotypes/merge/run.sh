vcf1=$1
vcf2=$2
Outh_path=$3
name=$4
bcftools merge $1 $2 -Oz --threads 15 -o $Outh_path/$name.bcf.gz
bcftools index --threads 15 $Outh_path/$name.bcf.gz