bsub -R'select[mem>50000] rusage[mem=50000]' -J ambientness  -n 1 -M 50000 -o ambientness.o -e ambientness.e -q normal python ./ambientness.py