

params {
    RUN = "$RUN_ID"
    PATH2 = "/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/fetch/${RUN}"
    input = 'cellbender' 
    lisi{
        run_process=false
    }
    replace_genotype_ids=false
    webtransfer = false
    write_h5=true
    encrypt = true
    project_name = 'Cardinal_Analysis'
    cellbender_location='' //!!!!! if cellbender is run already then can skip this by selecting  input = 'existing_cellbender' instead input = 'cellbender'
    cellbender_resolution_to_use='0pt1'
    extra_metadata = "$PATH2/results/yascp_inputs/Extra_Metadata.tsv"
    extra_sample_metadata ="$PATH2/results/yascp_inputs/Extra_Metadata_Donors.tsv"
    genotype_phenotype_mapping_file = '/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/secret/bridge.txt'
    
    run_celltype_assignment=true
    split_ad_per_bach=true //if not splitting the celltype assignment will be run on full tranche
    input_data_table = "$PATH2/results/yascp_inputs/input.tsv" //this has to be a full path
    run_with_genotype_input=true
	genotype_input {
        posterior_assignment = true //if this is set to true, we will perform the genotype donor matching after the deconvolution is performed.
        subset_genotypes = false //if activated this will use th IDs provided to estimate the donors, otherwise it will match against full cohort
        full_vcf_file = '/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/filtered_genotypes/vcf/merged_bcf/GT_AF_ELGH_Concat.bcf.gz' //this could be a list of vcfs, in which case have to merge them 
        tsv_donor_panel_vcfs = "/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/genotypes/donor_panels_vcf_paths.tsv"
    }
    souporcell {
        run = false
    }
    skip_preprocessing{
        value=false
        file__anndata_merged = ''
        file__cells_filtered = ''
    }
}

process {

    withName: plot_distributions{
        containerOptions = "--containall --cleanenv --workdir /tmp -B /tmp"
    }

    withName: cellex_cluster_markers{
        maxForks=7
        memory = 300.GB
    }
    
    withName: GATHER_DATA{
        maxForks=7
        memory = 100.GB
    }
    withName: LISI{
        maxForks=7
        memory = 500.GB
    }
    withName: cluster_validate_resolution_keras{
        memory = 300.GB
    }

    withName: umap_calculate_and_plot{
        memory = 300.GB
    }

    withName: sccaf_assess_clustering{
        memory = 300.GB
    }
    
}

singularity {
  enabled = true
  cacheDir   = "${baseDir}/singularity"
  runOptions = '--bind /lustre --no-home'
}