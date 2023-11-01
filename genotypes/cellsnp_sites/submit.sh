chr="14"
sample="sorted_hg38_ukb_imp_chr${chr}_v3"
bsub -R'select[mem>40000] rusage[mem=40000]' -J $sample.sub -n 5 -M 40000 -o $sample.o -e $sample.e -q long bash ./run.sh $sample $chr