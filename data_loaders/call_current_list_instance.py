import io
import random
import string
from typing import Dict, List
import pandas as pd
import json
import requests


if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(access_token, *args, **kwargs) -> List[List[Dict]]:
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
    amc_dict = []

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


    amc_instance_list = {customerName[i]: instanceId[i] for i in range(len(customerName))}  
    del amc_instance_list['Perpetua_Sandbox'] # get rid of this now
    AWS_HOSTS_DICT_flipped = {instanceId[i]: customerName[i] for i in range(len(instanceId))}
        

    return amc_instance_list
