from typing import Dict, List
import io
import pandas as pd
import requests

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@custom
def execute_workflow(data, *args, **kwargs):
    
    header_staple = {'Content-Type': 'application/x-amz.json-1.1',
                 'Amazon-Advertising-API-MarketplaceId': 'ATVPDKIKX0DER',
                 'instanceId': 'amcl5g0tpcp',
                'Amazon-Advertising-API-ClientId':'amzn1.application-oa2-client.7e844863cba54228a30de0805ef9f139',
                'Amazon-Advertising-API-AdvertiserId':'ENTITY2M6J5JPS44Y4R',
                'Authorization': f"Bearer {data['access_token']}"}
   
  
    post_data = {
        'workflowId': f"{data['full_workflow_name']}",
        'timeWindowType': "EXPLICIT",
        'timeWindowStart': "2023-08-01T00:00:00", # in mage variable from Aug 1 to Sept 1
        'timeWindowEnd': "2023-09-01T00:00:00", # in mage variable from Aug 1 to Sept 1
        "ignoreDataGaps": "true",
        "parameterValues": {
            "Advertiser": data['customer_name']
        }
    }
    workflow_execution_url =  f"https://advertising-api.amazon.com/amc/reporting/{data['instanceId']}/workflowExecutions"
    r = requests.post(
        workflow_execution_url, 
        json=post_data, 
        headers=header_staple,
    )

    if r.status_code == 200:
        print(r.text)
        print(f"Workflow <{data['full_workflow_name']}> executed successfully. Proceeding with workflow retrieve.")
        workflowExecutionId = r.json()['workflowExecutionId']
        data['workflowExecutionId'] = workflowExecutionId
        return data

    if r.status_code in {504, 503, 502, 500, 400}:
        print(f"Workflow <{data['full_workflow_name']}> returned bad status. Please investigate.")
        #to do - find out how to log in mage
        return data
       

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
