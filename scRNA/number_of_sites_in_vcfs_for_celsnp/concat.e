[E::idx_find_and_load] Could not retrieve index file for '/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc/genome1K.phase3.SNP_AF5e2.chr1toX.hg38.vcf.gz'
Traceback (most recent call last):
  File "/lustre/scratch123/hgi/mdt1/projects/ukbb_scrna/analysis/mo11/random/scRNA/number_of_sites_in_vcfs_for_celsnp/overlapping_sites.py", line 48, in <module>
    sites = get_field_info(rec)    
  File "/lustre/scratch123/hgi/mdt1/projects/ukbb_scrna/analysis/mo11/random/scRNA/number_of_sites_in_vcfs_for_celsnp/overlapping_sites.py", line 23, in get_field_info
    info_string+=f"{i_field}={rec.info['AF'][0]};"    
  File "pysam/libcbcf.pyx", line 2563, in pysam.libcbcf.VariantRecordInfo.__getitem__
KeyError: 'Unknown INFO field: AF'
[E::idx_find_and_load] Could not retrieve index file for '/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc/genome1K.phase3.SNP_AF5e2.chr1toX.hg38.vcf.gz'
Traceback (most recent call last):
  File "/lustre/scratch123/hgi/mdt1/projects/ukbb_scrna/analysis/mo11/random/scRNA/number_of_sites_in_vcfs_for_celsnp/overlapping_sites.py", line 48, in <module>
    sites = get_field_info(rec)    
  File "/lustre/scratch123/hgi/mdt1/projects/ukbb_scrna/analysis/mo11/random/scRNA/number_of_sites_in_vcfs_for_celsnp/overlapping_sites.py", line 23, in get_field_info
    info_string+=f"{i_field}={rec.info[i_field][0]};"    
TypeError: 'float' object is not subscriptable
