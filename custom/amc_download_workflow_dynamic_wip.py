if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@custom
def transform_custom(data, *args, **kwargs):
    try:
                workflow_status = json.loads(await resp.read())
                if workflow_status['status'] in {"PENDING", "RUNNING"}:
                    print(f'Checking workflow status for {instance_id_with_sql}...still running/pending.')
                    await asyncio.sleep(400)
                    return await check_for_report(workflowexecution_id, instance_id_with_sql)
                elif workflow_status['status'] in {"SUCCEEDED"}: # grab downloadUrls here
                    print(f'workflow status success for {instance_id_with_sql} Uploading to bucket.')
                    url_dl = f'https://advertising-api.amazon.com/amc/reporting/{instance_id_clean}/workflowExecutions/{workflowexecution_id}/downloadUrls'
                    async with session.get(url_dl, headers=header_staple, raise_for_status=False) as resp:

    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
