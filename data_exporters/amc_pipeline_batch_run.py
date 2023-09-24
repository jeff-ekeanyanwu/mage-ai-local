from mage_ai.orchestration.triggers.api import trigger_pipeline
if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def trigger(data, *args, **kwargs):
    """
    Trigger another pipeline to run.

    Documentation: https://docs.mage.ai/orchestration/triggers/trigger-pipeline
    """
    instanceId = data['instanceId']
    customer_name = data['customer_name']
    

    amc_instance_list = {customer_name: instanceId}

    for key, value in amc_instance_list.items():
        print(f"Running {key} - {kwargs['pipeline_name']} AMC report pipeline...")
        trigger_pipeline(
            kwargs['pipeline_name'],        # Required: enter the UUID of the pipeline to trigger
            variables={'customer_name': key, "instanceId": value, "query_start_date": kwargs['time_window_start'], "query_end_date": kwargs['time_window_end']} ,  # Optional: runtime variables for the pipeline
            check_status=False,     # Optional: poll and check the status of the triggered pipeline
            error_on_failure=False, # Optional: if triggered pipeline fails, raise an exception
            poll_interval=60,       # Optional: check the status of triggered pipeline every N seconds
            poll_timeout=None,      # Optional: raise an exception after N seconds
            verbose=True,           # Optional: print status of triggered pipeline run
        )
    return print(f"{kwargs['pipeline_name']} amc report call sent for {customer_name}.")
