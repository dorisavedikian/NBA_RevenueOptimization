SELECT
    g.game_date,
    g.opponent,
    SUM(t.revenue) AS total_revenue,
    SUM(t.seats_purchased) AS tickets_sold,
    ROUND(AVG(t.ticket_price),2) AS average_ticket_price
FROM fact_ticket_transactions t
JOIN dim_games g
ON t.game_id = g.game_id
GROUP BY
    g.game_date,
    g.opponent
ORDER BY total_revenue DESC;