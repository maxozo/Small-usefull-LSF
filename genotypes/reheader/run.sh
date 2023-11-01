sample=$1
outpath='/lustre/scratch123/hgi/projects/ukbiobank_genotypes/FullRelease/Imputed/VCFs/hg38_bcf'
input_path='/lustre/scratch123/hgi/projects/ukbiobank_genotypes/FullRelease/Imputed/VCFs/hg38'
bcftools view -h $input_path/$sample.vcf.gz > $outpath/header_$sample.txt
bcftools reheader --threads 10 -h $outpath/header_$sample.txt -o $outpath/$sample.vcf $input_path/$sample.vcf.gz 
# sort now and export as bcf
bcftools sort $outpath/$sample.vcf -Ob -o $outpath/$sample.bcf.gz
bcftools index --threads 10 $outpath/$sample.bcf.gz
# then index it