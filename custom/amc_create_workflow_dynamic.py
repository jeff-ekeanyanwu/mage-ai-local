from typing import Dict, List
import io
import pandas as pd
import requests

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test



@custom
def create_workflow(data, *args, **kwargs):

            
    header_staple = {'Content-Type': 'application/x-amz.json-1.1',
                 'Amazon-Advertising-API-MarketplaceId': 'ATVPDKIKX0DER',
                 'instanceId': 'amcl5g0tpcp',
                'Amazon-Advertising-API-ClientId':'amzn1.application-oa2-client.7e844863cba54228a30de0805ef9f139',
                'Amazon-Advertising-API-AdvertiserId':'ENTITY2M6J5JPS44Y4R',
                'Authorization': f"Bearer {data['access_token']}"}
        
    workflows_url = f"https://advertising-api.amazon.com/amc/reporting/{data['instanceId']}/workflows"

    post_data = {
    'workflowId': f"{data['full_workflow_name']}",
    'sqlQuery': data['sql_query'],
    'inputParameters': [
    {
    "name": "Advertiser",
    "dataType": "STRING",
    "columnType": "DIMENSION",
    "defaultValue": data['customer_name']
    }]}

    r = requests.post(
        workflows_url, 
        json=post_data, 
        headers=header_staple)

    if r.status_code == 200:
        print(f"{data['full_workflow_name']} - Workflow creation failed. Retrying.")
        return data
        
        
    if r.status_code in {504, 503, 502, 500, 400}:
        print(r.json())
        print(f"{data['full_workflow_name']} - Workflow creation failed. Retrying.")
        raise Exception
        


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
