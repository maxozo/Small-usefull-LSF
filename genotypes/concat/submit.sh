job='concat_ukbb_basement'
bsub -R'select[mem>60000] rusage[mem=60000]' -J $job  -n 6 -M 60000 -o $job.o -e $job.e -q basement bash ./run.sh