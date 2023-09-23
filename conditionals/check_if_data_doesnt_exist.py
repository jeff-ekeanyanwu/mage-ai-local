if 'condition' not in globals():
    from mage_ai.data_preparation.decorators import condition


@condition
def check_if_data_doesnt_exist(df, *args, **kwargs) -> bool:
    return len(df) == 0
