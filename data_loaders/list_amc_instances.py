import io
import pandas as pd
import json
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(access_token, *args, **kwargs):
    """
    Template for loading data from API
    """
    header_staple = {'Content-Type': 'application/x-amz.json-1.1',
                 'Amazon-Advertising-API-MarketplaceId': 'ATVPDKIKX0DER',
                 'instanceId': 'amcl5g0tpcp',
                'Amazon-Advertising-API-ClientId':'amzn1.application-oa2-client.7e844863cba54228a30de0805ef9f139',
                'Amazon-Advertising-API-AdvertiserId':'ENTITY2M6J5JPS44Y4R',
                'Authorization': f'Bearer {access_token}'}


    metadata_url = 'https://advertising-api.amazon.com/amc/instances'
    r = requests.get(
    metadata_url,
    headers=header_staple,
    )
    
    df = pd.json_normalize(r.json(), record_path=['instances'], sep='_')

    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
