tmp='/lustre/scratch123/hgi/projects/ukbiobank_genotypes/FullRelease/Imputed/VCFs/tmp/'
# bcftools filter -e 'MAF < 0.05' --threads 10 -Ob -o $2/$3.bcf $1
echo "bcftools annotate -x INFO,^FORMAT/GT,FORMAT/AF $2/$3.bcf -Ob --threads 10 -o $2/filt_$3.bcf"
bcftools annotate -x INFO,^FORMAT/GT,FORMAT/AF $2/$3.bcf -Ob --threads 10 -o $2/filt_$3.bcf
# echo bcftools sort -T $tmp -Ob -o $2/srt_$3.bcf.gz filt_$2/$3.bcf
bcftools sort -T $tmp -Ob -o $2/srt_$3.bcf.gz $2/filt_$3.bcf
# bcftools annotate -x INFO,^FORMAT/GT,FORMAT/AF $1 -Ob --threads 10 -o $2
