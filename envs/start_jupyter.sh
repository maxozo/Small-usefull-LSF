#!/usr/bin/env bash
set -e
set -u
set -o pipefail

CWD1=$PWD
MY_PATH="$(dirname -- "${BASH_SOURCE[0]}")"            # relative
MY_PATH="$(cd -- "$MY_PATH" && pwd)"    # absolutized and normalized
# defaults
cd $MY_PATH
notebookdir=$CWD1
condaenv=/software/hgi/installs/anaconda3/envs/mo11

while getopts 'g:c:m:q:d:e:' OPTION; do
  case "$OPTION" in
    g)
      lsf_group="$OPTARG"
      echo "LSF group is $lsf_group"
      ;;
    c)
      n_cpus="$OPTARG"
      echo "Number of requested CPUs is $n_cpus"
      ;;
    m)
      mem="$OPTARG"
      echo "LSF memory requested is $mem"
      ;;
    q)
      queue="$OPTARG"
      echo "LSF queue requested is $queue"
      ;;
    d)
      notebookdir="$OPTARG"
      ;; 
    e)
      condaenv="$OPTARG"
      ;;
  esac
done
shift "$(($OPTIND -1))"

echo starting bsub...
rm -f jupyter_lab.log
echo "notebook dir will be $notebookdir"
echo "jupyter lab conda env is $condaenv"

bash jupyter_lab.sh -d $notebookdir -e $condaenv
echo waiting for LSF job to start... >> jupyter_lab.log
echo finished bsub
echo see file jupyter_lab.log for jupyterhub IP address and port
tail -f jupyter_lab.log