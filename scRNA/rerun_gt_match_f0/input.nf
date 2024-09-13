params{
    file_name = "$FILE"
    vcf = "$PWD/../${FILE}_headfix_vireo.vcf.gz"
    genotype_input {
        tsv_donor_panel_vcfs = "/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/qc_F0_reruns/donor_panels_vcf_path2.tsv"
    }
    input_data_table = "$PWD/../../../Summary_plots/Fetch/Input/input_table.tsv" //this has to be a full path
    genotype_phenotype_mapping_file = '/lustre/scratch123/hgi/projects/ukbb_scrna/pipelines/Pilot_UKB/secret/bridge_06_03_2024.tsv'
    copy_mode = "copy"
}

process{

    withName: GT_MATCH_POOL_AGAINST_PANEL{
        time   = { 2.h   * task.attempt }
        maxRetries    = 2
    }

}