shopt -s nullglob
for dir in /lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc/All_Cardinal_pilot_runs/*/
do
    part2=$(basename "$dir")
    echo $part2
    echo $dir
    bsub -R'select[mem>4000] rusage[mem=4000]' -J $part2.compress -n 1 -M 4000 -o $part2.o -e $part2.e -q long bash ./run.sh $part2 $dir 
done

# bsub -R'select[mem>40000] rusage[mem=40000]' -J subset -n 1 -M 40000 -o subset.o -e subset.e -q normal bash ./run.sh