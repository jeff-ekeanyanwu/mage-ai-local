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
    header_staple = {'Content-Type': 'application/x-amz.json-1.1',
                 'Amazon-Advertising-API-MarketplaceId': 'ATVPDKIKX0DER',
                 'instanceId': 'amcl5g0tpcp',
                'Amazon-Advertising-API-ClientId':'amzn1.application-oa2-client.7e844863cba54228a30de0805ef9f139',
                'Amazon-Advertising-API-AdvertiserId':'ENTITY2M6J5JPS44Y4R',
                'Authorization': f"Bearer {data['access_token']}"}

    url = f'https://advertising-api.amazon.com/amc/reporting/{instance_id_clean}/workflowExecutions/{workflowexecution_id}'
    r = requests.get(
        url,
        headers=header_staple,
    )
    try:
                workflow_status = json.loads(await resp.read())
                if workflow_status['status'] in {"PENDING", "RUNNING"}:
                    print(f'Checking workflow status for {instance_id_with_sql}...still running/pending.')
                    await asyncio.sleep(400)
                    return await check_for_report(workflowexecution_id, instance_id_with_sql)
                elif workflow_status['status'] in {"SUCCEEDED"}: # grab downloadUrls here
                    print(f'workflow status success for {instance_id_with_sql} Uploading to bucket.')
                    url_dl = f'https://advertising-api.amazon.com/amc/reporting/{instance_id_clean}/workflowExecutions/{workflowexecution_id}/downloadUrls'


    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
