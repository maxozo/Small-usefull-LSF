#!/bin/bash

# find /lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/hp3_dev/nf_core_rnaseq_repl/ -maxdepth 8 -mindepth 1 -type f -exec touch {} +
# find ./pipelines/hp3_dev/nf_core_rnaseq_repl/ref/ -maxdepth 8 -mindepth 1 -type f -exec touch {} +

# find . -maxdepth 8 -mindepth 1 -type f -exec touch {} +

set -e

ndays_oldest=95
echo aims to set oldest file to now - $ndays_oldest days
root_dir=/lustre/scratch123/hgi/projects/ukbb_scrna
echo root_dir is $root_dir

# oldest file by mtime, exclude .vault files
echo looking for oldest file..
oldest_file=$(find ${root_dir}/ -not -path "${root_dir}/.vault/*" -type f -printf '%T+ %p\n' | sort | head -n 1 | cut -f2 -d" ")
echo oldest_file is $oldest_file

filemtime=$(stat -c %Y $oldest_file)
filemtime_y=$(stat -c %y $oldest_file)
echo oldest_file mtime is $filemtime $filemtime_y

current_time=`date +%s`
echo current_time is $current_time $(date -d @$current_time)

diff=$(( (current_time - filemtime)/(60*60*24) ))
echo current time - file mtime is $diff days

days_to_add=$(( (diff - ndays_oldest) ))
echo days_to_add is $days_to_add
seconds_to_add=$(( (days_to_add)*(60*60*24) ))
echo which is $seconds_to_add seconds

newmtime=$(( (filemtime + seconds_to_add) )) 
echo new shifted mtime is $newmtime $(date -d @$newmtime)
touch newfile
echo before $(stat -c %y newfile)
touch --date=@$newmtime newfile
echo after $(stat -c %y newfile)

