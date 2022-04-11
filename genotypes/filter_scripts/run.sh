bcftools annotate -x INFO,^FORMAT/GT,FORMAT/AF $1 -Oz --threads 5 -o $2
