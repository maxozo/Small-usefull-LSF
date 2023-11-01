sample='hg38_ukb_imp_chr7_v3'
bsub -R'select[mem>40000] rusage[mem=40000]' -J sort_$sample -n 10 -M 40000 -o sort_$sample.o -e sort_$sample.e -q long bash ./run.sh $sample