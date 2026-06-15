SELECT
    p.promotion_name,
    COUNT(*) AS transactions,
    ROUND(AVG(t.ticket_price),2) AS avg_ticket_price,
    SUM(t.revenue) AS total_revenue
FROM fact_ticket_transactions t
JOIN dim_promotions p
ON t.promotion_id = p.promotion_id
GROUP BY
    p.promotion_name
ORDER BY total_revenue DESC;