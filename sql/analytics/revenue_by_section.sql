SELECT
    s.section_name,
    COUNT(*) AS transactions,
    SUM(t.seats_purchased) AS tickets_sold,
    ROUND(AVG(t.ticket_price),2) AS avg_price,
    SUM(t.revenue) AS total_revenue
FROM fact_ticket_transactions t
JOIN dim_sections s
ON t.section_id = s.section_id
GROUP BY s.section_name
ORDER BY total_revenue DESC;