import io
import random
import string
from typing import Dict, List
import pandas as pd
import json
import requests
from time import sleep
from random import randint

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@custom
def delete_workflow(data, *args, **kwargs):
    
    """
    Args:
        data: The output from the upstream parent block (if applicable)
        args: The output from any additional upstream blocks

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    #logger = kwargs.get('logger')

    # Sleep a random number of seconds (between 20 and 70) for rate limiting


    instanceId = data['instanceId']
    customer_name = data['customer_name']

    full_workflow_name = str(data['customer_name'])+str(data['query_name'])
    
    header_staple = {'Content-Type': 'application/x-amz.json-1.1',
                 'Amazon-Advertising-API-MarketplaceId': 'ATVPDKIKX0DER',
                 'instanceId': 'amcl5g0tpcp',
                'Amazon-Advertising-API-ClientId':'amzn1.application-oa2-client.7e844863cba54228a30de0805ef9f139',
                'Amazon-Advertising-API-AdvertiserId':'ENTITY2M6J5JPS44Y4R',
                'Authorization': f"Bearer {data['access_token']}"}
    
# the full_workflow_name was a combination of customer_name+file_in_sql
    # to delete a previous workflow, we now call this instead:
    delete_workflow_url = f"https://advertising-api.amazon.com/amc/reporting/{instanceId}/workflows/{full_workflow_name}"
    r = requests.delete(
        delete_workflow_url, 
        headers=header_staple,
    )
    if r.status_code == 200: # this is because it would appear that the DELETE request returns no response when 200
        #logger.info(f"Workflow <{full_workflow_name}> deleted successfully. Proceeding with workflow create.")
        data['full_workflow_name'] = full_workflow_name
        return data
    
    if r.status_code in {504, 503, 502, 500, 429, 423}:
        #logger.warning(f"Error deleting workflow <{full_workflow_name}>. Attempting to retry: {r.text}")
        data['full_workflow_name'] = full_workflow_name
        raise Exception

    if r.status_code == 400: # totally fine to error here, just means it's the first time creating the workflow in most cases
        #logger.warning(f'Error deleting workflow <{full_workflow_name}>. Attempting to proceed with workflow create: {r.text}')
        data['full_workflow_name'] = full_workflow_name
        return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
