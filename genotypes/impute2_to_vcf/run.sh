# bcftools annotate -x INFO,^FORMAT/GT,FORMAT/AF $1 -Oz --threads 5 -o $2
bcftools convert --haplegendsample2vcf $1/$2.hap.gz,$1/$2.legend.gz,$1/$2.samples --threads 5 -Oz -o $3/chr$2_uk10k_1000g_phase3.vcf.gz
