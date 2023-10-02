if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@custom
def custom_sql_query():
    sql_query = "WITH sp_ids as (SELECT distinct campaign FROM sponsored_ads_traffic ), dsp_ids as (SELECT distinct campaign_id FROM dsp_impressions ) , dsp_ntb as ( select '1' as join_key, COUNT(DISTINCT user_id) as dsp_ntb_users from amazon_attributed_events_by_conversion_time where new_to_brand=true and purchases>0 and campaign_id in (select campaign_id from dsp_ids) group by 1 ), sp_ntb as ( select '1' as join_key, COUNT(DISTINCT user_id) as sp_ntb_users from amazon_attributed_events_by_conversion_time where new_to_brand=true and purchases>0 and ad_product_type = 'sponsored_products' group by 1 ), dsp_cost as ( SELECT '1' as join_key, currency_name, currency_iso_code, sum(impression_cost/100000) AS dsp_impression_cost, sum(total_cost/100000) AS dsp_total_cost, sum(supply_cost/100000000) as dsp_supply_cost, sum(audience_fee/100000000) as dsp_audience_fee, sum(platform_fee/100000000) as dsp_platform_fee, sum(third_party_fees/100000000) as dsp_third_party_fees FROM dsp_impressions where campaign_id in (select campaign_id from dsp_ids) GROUP BY join_key, currency_name, currency_iso_code ) , sp_cost as ( SELECT '1' as join_key, currency_name, currency_iso_code, 0 as dsp_impression_cost, 0 as dsp_total_cost, 0 as dsp_supply_cost, 0 as dsp_audience_fee, 0 as dsp_platform_fee, 0 as dsp_third_party_fees, SUM(spend/100000000) AS sp_spend FROM sponsored_ads_traffic s GROUP BY join_key, currency_iso_code, currency_name ), final_data as ( select i.join_key, currency_name, currency_iso_code, dsp_ntb_users, 0 as sp_ntb_users, dsp_impression_cost, dsp_total_cost, dsp_supply_cost, dsp_audience_fee, dsp_platform_fee, dsp_third_party_fees, 0 as sp_spend from dsp_cost i left join dsp_ntb n on i.join_key=n.join_key union all select s.join_key, currency_name, currency_iso_code, 0 as dsp_ntb_users, sp_ntb_users, dsp_impression_cost, dsp_total_cost, dsp_supply_cost, dsp_audience_fee, dsp_platform_fee, dsp_third_party_fees, sp_spend from sp_cost s left join sp_ntb n on s.join_key=n.join_key ) select CAST(BUILT_IN_PARAMETER('TIME_WINDOW_START') as date) as start_date ,CAST(BUILT_IN_PARAMETER('TIME_WINDOW_END') as date) as end_date ,currency_name ,currency_iso_code ,sum(dsp_ntb_users) as dsp_ntb_users ,sum(sp_ntb_users) as sp_ntb_users ,sum(dsp_impression_cost) as dsp_impression_cost ,sum(dsp_total_cost) as dsp_total_cost ,sum(dsp_supply_cost) as dsp_supply_cost ,sum(dsp_audience_fee) as dsp_audience_fee ,sum(dsp_platform_fee) as dsp_platform_fee ,sum(dsp_third_party_fees) as dsp_third_party_fees ,sum(sp_spend) as sp_spend from final_data f group by 1,2,3,4"
    query_name = "cac_account_level"
    return [sql_query, query_name]


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'