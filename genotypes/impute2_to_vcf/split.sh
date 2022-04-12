while read p; do
#   echo "$p"
  A="$(cut -d':' -f1 <<< $p)"
  
echo  "$A $p"
done </lustre/scratch123/hgi/projects/bhf_finemap/imputation/uk10k_1000g_phase3/21_all.hap
