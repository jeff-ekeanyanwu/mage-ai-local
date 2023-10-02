import time
from typing import Dict, List
import io
import pandas as pd
import requests
import json
from time import sleep
from random import randint

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@custom
def transform_custom(data, *args, **kwargs):
    """
    Args:
        data: The output from the upstream parent block (if applicable)
        args: The output from any additional upstream blocks

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """

    # Sleep a random number of seconds (between 20 and 70) for rate limiting???
    #sleep(randint(20,70))


    header_staple = {'Content-Type': 'application/x-amz.json-1.1',
                 'Amazon-Advertising-API-MarketplaceId': 'ATVPDKIKX0DER',
                 'instanceId': 'amcl5g0tpcp',
                'Amazon-Advertising-API-ClientId':'amzn1.application-oa2-client.7e844863cba54228a30de0805ef9f139',
                'Amazon-Advertising-API-AdvertiserId':'ENTITY2M6J5JPS44Y4R',
                'Authorization': f"Bearer {data['access_token']}"}

    url = f"https://advertising-api.amazon.com/amc/reporting/{data['instanceId']}/workflowExecutions/{data['workflowExecutionId']}"
    r = requests.get(
        url,
        headers=header_staple,
    )
    logger = kwargs.get('logger')
    

    try:
        if r.status_code == 200:
            workflow_status = r.json().get("status")
            while workflow_status in {"PENDING", "RUNNING"}:
                print(f"Checking workflow status for {data['full_workflow_name']}...still running/pending.")
                time.sleep(200)
                r = requests.get(url, headers=header_staple)
                workflow_status = r.json().get("status")
                if workflow_status in {"CANCELLED"}:
                    print(f"Workflow fatally cancelled for {data['full_workflow_name']}. Please investigate.")
                    data['retrieve_workflow_status'] = "failed"
                    raise Exception
                if workflow_status in {"SUCCEEDED"}:
                    print(f"workflow status success for {data['full_workflow_name']} Uploading to BigQuery.")
                    data['retrieve_workflow_status'] = "success"
                    url_dl = f"https://advertising-api.amazon.com/amc/reporting/{data['instanceId']}/workflowExecutions/{data['workflowExecutionId']}/downloadUrls"
                    r = requests.get(url_dl, headers=header_staple)
                    download_url = r.json()["downloadUrls"][0]
                    try:
                        df = pd.read_csv(download_url,on_bad_lines='error')
                        if 'instanceId' not in df:
                            df['instanceId'] = kwargs['instanceId']
                        return df
                    except:
                        print(f"{kwargs['customer_name']} has no values to return! OR there is an error in this csv! Ending pipeline gracefully.")
                        df = pd.DataFrame()
                        return df
            if workflow_status in {"CANCELLED"}:
                    print(f"Workflow fatally cancelled for {data['full_workflow_name']}. Please investigate.")
                    data['retrieve_workflow_status'] = "failed"
                    raise Exception
            if workflow_status in {"SUCCEEDED"}:
                    print(f"workflow status success for {data['full_workflow_name']} Uploading to BigQuery.")
                    data['retrieve_workflow_status'] = "success"
                    url_dl = f"https://advertising-api.amazon.com/amc/reporting/{data['instanceId']}/workflowExecutions/{data['workflowExecutionId']}/downloadUrls"
                    r = requests.get(url_dl, headers=header_staple)
                    download_url = r.json()["downloadUrls"][0]
                    try:
                        df = pd.read_csv(download_url,on_bad_lines='error')
                        if 'instanceId' not in df:
                            df['instanceId'] = kwargs['instanceId']
                        return df
                    except:
                        print(f"{kwargs['customer_name']} has no values to return! OR there is an error in this csv! Ending pipeline gracefully.")
                        df = pd.DataFrame()
                        return df
            
            
    except AttributeError:
       logger.error(f"{r.status_code} for {data['full_workflow_name']}. Please retry. {r.text}" )

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
