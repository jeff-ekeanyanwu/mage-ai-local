import io
import pandas as pd
import requests
import yaml
import json
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@custom
def get_access_token():

    # Note: You need to have the yaml file with the tokens on it to run this if you are not running it here

    full_file_path = r"/home/secrets/secrets (2).yaml"
    with open(full_file_path) as settings:
        settings_data = yaml.load(settings, Loader=yaml.Loader)


    p_refresh_token = settings_data['refresh_token']
    p_client_id = settings_data['client_id']
    p_client_secret = settings_data['client_secret']


    token_auth_url = 'https://api.amazon.com/auth/o2/token'

    post_objects = {'grant_type':'refresh_token', 
                    'refresh_token': str(f'{p_refresh_token}'),
                    'client_id': str(f'{p_client_id}'),
                    'client_secret': str(f'{p_client_secret}')}

    r = requests.post(
        token_auth_url,
        post_objects)

    json_formatted_str = json.dumps(r.json(), indent=2)
    p_access_token = r.json().get("access_token")
    return p_access_token

access_token = get_access_token()

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'

