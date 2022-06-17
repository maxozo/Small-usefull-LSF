bsub -R'select[mem>40000] rusage[mem=40000]' -J sort2  -n 5 -M 40000 -o sort2.o -e sort2.e -q normal bash ./run.sh \
   /lustre/scratch123/hgi/projects/bhf_finemap/imputation/uk10k_1000g_blueprint/uk10k_1000g_blueprint.bcf.gz \
    uk10k_1000g_blueprint \
    /lustre/scratch123/hgi/projects/bhf_finemap/imputation/uk10k_1000g_blueprint