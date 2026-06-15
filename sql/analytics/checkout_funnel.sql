SELECT
    COUNT(*) AS sessions,
    SUM(added_to_cart) AS cart_adds,
    SUM(checkout_started) AS checkouts,
    SUM(purchased) AS purchases,
    ROUND(100.0*SUM(added_to_cart)/COUNT(*),2) AS cart_rate,
    ROUND(100.0*SUM(checkout_started)/SUM(added_to_cart),2) AS checkout_rate,
    ROUND(100.0*SUM(purchased)/SUM(checkout_started),2) AS purchase_rate
FROM fact_web_sessions;