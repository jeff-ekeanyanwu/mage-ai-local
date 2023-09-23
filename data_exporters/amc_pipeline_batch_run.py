from mage_ai.orchestration.triggers.api import trigger_pipeline
if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def trigger(amc_instance_list,*args, **kwargs):
    """
    Trigger another pipeline to run.

    Documentation: https://docs.mage.ai/orchestration/triggers/trigger-pipeline
    """
    for key, value in amc_instance_list.items():
        print(f"Running {key} bof_purchases AMC report pipeline...")
        trigger_pipeline(
            'bof_purchases',        # Required: enter the UUID of the pipeline to trigger
            variables={'customer_name': key, "instanceId": value, "query_start_date": "2023-04-01T00:00:00", "query_end_date": "2023-06-30T00:00:00"} ,  # Optional: runtime variables for the pipeline
            check_status=False,     # Optional: poll and check the status of the triggered pipeline
            error_on_failure=False, # Optional: if triggered pipeline fails, raise an exception
            poll_interval=60,       # Optional: check the status of triggered pipeline every N seconds
            poll_timeout=None,      # Optional: raise an exception after N seconds
            verbose=True,           # Optional: print status of triggered pipeline run
        )
    return print('All runs complete')
