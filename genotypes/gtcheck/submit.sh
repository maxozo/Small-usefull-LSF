sample='GT'
bsub -R'select[mem>40000] rusage[mem=40000]' -J $sample -n 2 -M 40000 -o $sample.o -e $sample.e -q normal bash ./run.sh