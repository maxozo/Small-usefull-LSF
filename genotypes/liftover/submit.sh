bsub -R'select[mem>40000] rusage[mem=40000]' -J liftover  -n 3 -M 40000 -o liftover.o -e liftover.e -q long bash ./run.sh /lustre/scratch123/hgi/projects/bhf_finemap/imputation/uk10k_1000g_phase3/vcfs/merged/uk10k_1000g_phase3_Concat.vcf.gz uk10k_1000g_phase3_Concat /lustre/scratch123/hgi/projects/bhf_finemap/imputation/uk10k_1000g_phase3/vcf_hg38