SELECT * FROM (SELECT DISTINCT stock_resource.*,iseq_run_lane_metrics.qc_complete as iseq_run_lane_metrics_qc_complete,sample.id_sample_tmp as sample_id_sample_tmp,iseq_flowcell.recorded_at as iseq_flowcell_recorded_at,sample.recorded_at as sample_recorded_at, donors.id_sample_tmp as tmp2,sample.name as experiment_id,original_study.name as cohort2,donors.customer_measured_volume as vol2,donors.supplier_name as donor 
FROM mlwarehouse.iseq_flowcell
 JOIN mlwarehouse.sample ON iseq_flowcell.id_sample_tmp = sample.id_sample_tmp 
 JOIN mlwarehouse.study ON iseq_flowcell.id_study_tmp = study.id_study_tmp 
 JOIN mlwarehouse.iseq_product_metrics ON iseq_flowcell.id_iseq_flowcell_tmp = iseq_product_metrics.id_iseq_flowcell_tmp
 JOIN mlwarehouse.iseq_run on iseq_run.id_run = iseq_product_metrics.id_run
 JOIN mlwarehouse.iseq_run_lane_metrics on iseq_run_lane_metrics.id_run = iseq_run.id_run
 JOIN mlwarehouse.psd_sample_compounds_components pscc ON iseq_flowcell.id_sample_tmp = pscc.compound_id_sample_tmp
 JOIN mlwarehouse.sample as donors ON donors.id_sample_tmp = pscc.component_id_sample_tmp
 JOIN mlwarehouse.stock_resource ON donors.id_sample_tmp = stock_resource.id_sample_tmp
 JOIN mlwarehouse.study as original_study ON original_study.id_study_tmp = stock_resource.id_study_tmp
 WHERE sample.name IN ('CRD_CMB13195930','CRD_CMB13195926','CRD_CMB13195922','CRD_CMB13195927','CRD_CMB13195928','CRD_CMB13195921','CRD_CMB13195929','CRD_CMB13195924','CRD_CMB13195920','CRD_CMB13195925','CRD_CMB13195923','CRD_CMB13195918','CRD_CMB13195919')
 AND donors.supplier_name LIKE "%30007454087%") as A
 LEFT JOIN (SELECT *,CONCAT(value,' ',units) as 'live_cell_count' from mlwarehouse.qc_result  WHERE qc_type = 'live_cell_count') as B on A.tmp2 = B.id_sample_tmp;