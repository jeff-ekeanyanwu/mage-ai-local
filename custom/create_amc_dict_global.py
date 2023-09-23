if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@custom
def transform_custom(access_token, data_2, *args, **kwargs):
    """
    Args:
        data: The output from the upstream parent block (if applicable)
        args: The output from any additional upstream blocks

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """

    sql_query = data_2[0]
    query_name = data_2[1]

    amc_instance_dict = {"customer_name": kwargs['customer_name'], "instanceId": kwargs['instanceId'], "sql_query": sql_query, "query_name": query_name, "access_token": access_token }

    return amc_instance_dict


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
