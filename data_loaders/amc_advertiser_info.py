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

    list_of_instances_info = []
    combined_dataframe = []

    metadata_url = 'https://advertising-api.amazon.com/amc/instances'
    r = requests.get(
        metadata_url,
        headers=header_staple,
    )

    json_formatted_str = json.dumps(r.json(), indent=2)

    data = json.loads(json_formatted_str)

    customerName = []
    apiEndpoint = []
    instanceId = []

    instance_search = data["instances"]
    for j in range(len(instance_search)):
        instanceId.append(instance_search[j]["instanceId"])

    instance_search = data["instances"]
    for i in range(len(instance_search)):
        safe_string_1 = instance_search[i]["customerCanonicalName"].replace(" ", "_")
        safe_string_2 = safe_string_1.replace("&", "").replace("(", "").replace(")", "")
        safe_string_3 = safe_string_2.replace("!", "i")
        customerName.append(safe_string_3)
        apiEndpoint.append(instance_search[i]["apiEndpoint"])


    AWS_HOSTS_DICT_2 = {customerName[i]: instanceId[i] for i in range(len(customerName))}  
    del AWS_HOSTS_DICT_2['Perpetua_Sandbox'] # get rid of this now
    AWS_HOSTS_DICT_flipped = {instanceId[i]: customerName[i] for i in range(len(instanceId))}

    for key,value in AWS_HOSTS_DICT_2.items():
        
        metadata_url = f'https://advertising-api.amazon.com/amc/instances/{value}/advertisers'
        r = requests.get(
        metadata_url,
        headers=header_staple,
        )
        
        json_formatted_str = json.dumps(r.json())

        df_key = pd.read_json(json_formatted_str)
        normalized_df_key = pd.json_normalize(df_key['advertisers'])
        normalized_df_key['instanceId'] = str(value)
        combined_dataframe.append(normalized_df_key)
        
        advertiser_list = pd.concat(combined_dataframe)

    return advertiser_list


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
