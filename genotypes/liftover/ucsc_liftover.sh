liftOver input.bed ~/storage/Downloaded_data/Liftover_chain/hg38ToHg19.over.chain.gz output.bed unlifted.bed
The input.bed
# input BED format file:
chrom   chromStart   chromEnd  name
chr[number]  POS -1 POS  rsid
# Download the chain file
wget http://hgdownload.soe.ucsc.edu/goldenPath/hg19/liftOver/hg19ToHg38.over.chain.gz