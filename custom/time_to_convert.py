if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@custom
def custom_sql_query():
    sql_query = "WITH get_date AS ( SELECT advertiser, campaign, ad_product_type, conversion_event_dt, CASE WHEN ad_product_type IN('sponsored_products','sponsored_display','sponsored_brands') THEN click_dt ELSE impression_dt END AS event_dt, total_purchases FROM TABLE(EXTEND_TIME_WINDOW('amazon_attributed_events_by_conversion_time', 'P60D', 'P0D')) ) SELECT advertiser, campaign, case when campaign similar to '_STV$' then 'STV' when campaign similar to '_OLV$' then 'OLV' when campaign similar to '_MOF$' then 'MOF' when campaign similar to '_TOF$'then 'Top of Funnel (Non-Video)' when campaign similar to '_BOF$' then 'Bottom of Funnel' when ad_product_type = 'sponsored_products' then 'SP' when ad_product_type = 'sponsored_display' then 'SD' when ad_product_type = 'sponsored_brands' then 'SB' else campaign end as campaign_type, CASE WHEN SECONDS_BETWEEN (event_dt, conversion_event_dt) <= 86400 THEN '< 24 HRS' WHEN SECONDS_BETWEEN (event_dt, conversion_event_dt) <= 259200 THEN '1 - 3 DAYS' WHEN SECONDS_BETWEEN (event_dt, conversion_event_dt) <= 604800 THEN '3 - 7 DAYS' WHEN SECONDS_BETWEEN (event_dt, conversion_event_dt) <= 1209600 THEN '7 - 14 DAYS' WHEN SECONDS_BETWEEN (event_dt, conversion_event_dt) <= 1814400 THEN '14 - 21 DAYS' WHEN SECONDS_BETWEEN (event_dt, conversion_event_dt) <= 2419200 THEN '21 - 28 DAYS' ELSE '28+ DAYS' END AS time_to_conversion, CASE WHEN SECONDS_BETWEEN (event_dt, conversion_event_dt) <= 86400 THEN '1 | < 24 HRS' WHEN SECONDS_BETWEEN (event_dt, conversion_event_dt) <= 259200 THEN '2 | 1 - 3 DAYS' WHEN SECONDS_BETWEEN (event_dt, conversion_event_dt) <= 604800 THEN '3 | 3 - 7 DAYS' WHEN SECONDS_BETWEEN (event_dt, conversion_event_dt) <= 1209600 THEN '4 | 7 - 14 DAYS' WHEN SECONDS_BETWEEN (event_dt, conversion_event_dt) <= 1814400 THEN '5 | 14 - 21 DAYS' WHEN SECONDS_BETWEEN (event_dt, conversion_event_dt) <= 2419200 THEN '6 | 21 - 28 DAYS' ELSE '7 | 28+ DAYS' END AS conversion_bucket, SUM(total_purchases) AS total_brand_purchases FROM get_date GROUP BY advertiser, campaign, campaign_type, time_to_conversion, conversion_bucket"
    query_name = "time_to_convert"
    return [sql_query, query_name]


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
