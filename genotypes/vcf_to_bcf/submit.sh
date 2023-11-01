sample='hg38_ukb_imp_chr20_v3'
bsub -R'select[mem>40000] rusage[mem=40000]' -J $sample/vcf_to_bcf -n 20 -M 40000 -o $sample.o -e $sample.e -q long bash ./run.sh $sample