from typing import Dict, List
import io
import pandas as pd
import requests
from time import sleep
from random import randint

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@custom
def execute_workflow(data, *args, **kwargs):


    # Sleep a random number of seconds (between 20 and 100) for rate limiting
    #sleep(randint(20,70))

    logger = kwargs.get('logger')
    
    header_staple = {'Content-Type': 'application/x-amz.json-1.1',
                 'Amazon-Advertising-API-MarketplaceId': 'ATVPDKIKX0DER',
                 'instanceId': 'amcl5g0tpcp',
                'Amazon-Advertising-API-ClientId':'amzn1.application-oa2-client.7e844863cba54228a30de0805ef9f139',
                'Amazon-Advertising-API-AdvertiserId':'ENTITY2M6J5JPS44Y4R',
                'Authorization': f"Bearer {data['access_token']}"}
   
  
    post_data = {
        'workflowId': f"{data['full_workflow_name']}",
        'timeWindowType': "EXPLICIT",
        'timeWindowStart': kwargs['query_start_date'], # in mage variable from Aug 1 to Sept 1
        'timeWindowEnd': kwargs['query_end_date'], # in mage variable from Aug 1 to Sept 1
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
        #logger.info(f"Workflow <{data['full_workflow_name']}> executed successfully. Proceeding with workflow retrieve: {r.text}")
        workflowExecutionId = r.json()['workflowExecutionId']
        data['workflowExecutionId'] = workflowExecutionId
        return data

    if r.status_code in {504, 503, 502, 500}:
        logger.warning(f"Workflow <{data['full_workflow_name']}> returned bad status. Please investigate. {r.text}")
        raise Exception
    
    if r.status_code == 400:
        
        logger.warning(f"Workflow <{data['full_workflow_name']}> returned bad status. Please investigate. {r.text}")
        try:
            workflowExecutionId = r.json()['workflowExecutionId']
            data['workflowExecutionId'] = workflowExecutionId
            return data
        except:
            logger.error(f"Workflow <{data['full_workflow_name']}> returned bad status. Please investigate. {r.text}")
            raise Exception

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
