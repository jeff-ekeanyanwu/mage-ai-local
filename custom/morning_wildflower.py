import mage_ai

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@custom
def transform_custom(amc_instance_list, *args, **kwargs):
    """
    Args:
        data: The output from the upstream parent block (if applicable)
        args: The output from any additional upstream blocks

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    for key, value in amc_instance_list.items():
        mage_ai.run('pipelines/customer_search_term_trigger_v2', 'repos/default_repo', customer_name=key, instanceId=value)

    return print('All runs successful.')