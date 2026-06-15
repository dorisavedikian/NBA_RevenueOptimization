SELECT
    device,
    COUNT(*) AS sessions,
    SUM(added_to_cart) AS carts,
    SUM(checkout_started) AS checkouts,
    SUM(purchased) AS purchases,
    ROUND(100.0*SUM(purchased)/COUNT(*),2) AS conversion_rate
FROM fact_web_sessions
GROUP BY device
ORDER BY conversion_rate DESC;