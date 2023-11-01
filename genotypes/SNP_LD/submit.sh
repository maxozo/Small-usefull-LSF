t='bed'
bsub -R'select[mem>40000] rusage[mem=40000]' -J $t  -n 3 -M 40000 -o $t.o -e $t.e -q long bash ./run.sh