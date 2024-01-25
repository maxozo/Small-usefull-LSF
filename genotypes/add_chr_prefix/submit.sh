for VARIABLE in $(ls /lustre/scratch125/humgen/teams/hgi/ip13/1k1k/with_GT/results/subset_genotypes/Genotype___AllExpectedGT_*/*.vcf.gz)
do
    echo $VARIABLE
    bsub -R'select[mem>10000] rusage[mem=10000]' -J sub -n 2 -M 10000 -o sub.o -e sub.e -q normal bash recode.sh $VARIABLE
    echo "submitted"
done