
# for cc in {1..22}
# do
# bsub -R'select[mem>40000] rusage[mem=40000]' -J $cc.sub -n 3 -M 40000 -o $cc.o -e $cc.e -q normal bash run_comand.sh $cc
# done


# for cc in {1..22}
# do
bsub -R'select[mem>40000] rusage[mem=40000]' -J cc.sub -n 3 -M 40000 -o cc.o -e cc.e -q yesterday bash run_comand.sh
# done