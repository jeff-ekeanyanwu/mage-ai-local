from pandas import DataFrame

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def concat_dataframes(df: DataFrame, *args, **kwargs):
    """
    Concatenate all dataframes returned by dynamic child blocks.
    """
    dataframes = kwargs[df]
    concatenated_df = pd.concat(dataframes)
    return concatenated_df



@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
