vcf1=$1
vcf2=$2
Outh_path=$3
bcftools merge $1 $2 -Oz --threads 15 -o $Outh_path/uk10k_1000g_blueprint.vcf.gz
