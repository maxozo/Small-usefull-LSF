bsub -R'select[mem>40000] rusage[mem=40000]' -J liftover  -n 3 -M 40000 -o liftover.o -e liftover.e -q long bash ./run.sh /lustre/scratch123/hgi/projects/bhf_finemap/imputation/blueprint/vcf/vcfblueprint_wp10_phase2_Concat.vcf.gz vcfblueprint_wp10_phase2_Concat /lustre/scratch123/hgi/projects/bhf_finemap/imputation/blueprint/vcf_hg38