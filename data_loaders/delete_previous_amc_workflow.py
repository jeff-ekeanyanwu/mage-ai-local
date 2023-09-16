import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

#TODO: Find a way to get the dynamic block to 

@data_loader
def delete_workflow(access_token, full_workflow_name, instanceId):
    
    header_staple = {'Content-Type': 'application/x-amz.json-1.1',
                 'Amazon-Advertising-API-MarketplaceId': 'ATVPDKIKX0DER',
                 'instanceId': 'amcl5g0tpcp',
                'Amazon-Advertising-API-ClientId':'amzn1.application-oa2-client.7e844863cba54228a30de0805ef9f139',
                'Amazon-Advertising-API-AdvertiserId':'ENTITY2M6J5JPS44Y4R',
                'Authorization': f'Bearer {access_token}'}
    
# the full_workflow_name was a combination of customer_name+file_in_sql
    # to delete a previous workflow, we now call this instead:
    delete_workflow_url = f'https://advertising-api.amazon.com/amc/reporting/{instanceId}/workflows/{full_workflow_name}'
    r = requests.delete(
        delete_workflow_url, 
        headers=header_staple,
    )
    if r.status_code == 200: # this is because it would appear that the DELETE request returns no response when 200
        return print(f'Workflow <{amc_2_value}> deleted successfully. Proceeding with workflow create.')
    
    if r.status_code in {504, 503, 502, 500}:
        print(r.json())
        print(f'{amc_2_value} - Workflow deletion failed (internal server error). Retrying.')
        raise ValueError

    else: # totally fine to error here, just means it's the first time creating the workflow in most cases
        print(f'Error deleting workflow <{amc_2_value}>. Attempting to proceed with workflow create.')
        return print(r.json())

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'

