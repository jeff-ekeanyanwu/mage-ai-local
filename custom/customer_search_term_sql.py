@custom
def customer_search_term():
    sql_query = "select distinct entity_id, campaign, ad_product_type, placement_type, customer_search_term, traffic_event_date as event_date, count(distinct user_id) as search_users, sum(total_purchases) as purchases, count(distinct case when total_purchases > 0 then user_id end) as purchase_users, sum(case when new_to_brand = true then total_purchases else 0 end) as ntb_purchases, count(distinct case when new_to_brand = true and total_purchases > 0 then user_id end) as ntb_purchase_users from amazon_attributed_events_by_traffic_time where customer_search_term is not null group by campaign, placement_type, customer_search_term, event_date, ad_product_type, entity_id"
    query_name = "customer_search_term_sa"
    return [sql_query, query_name]