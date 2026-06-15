SELECT
    g.opponent,
    SUM(t.revenue) AS revenue,
    SUM(t.seats_purchased) AS tickets_sold,
    ROUND(AVG(t.ticket_price),2) AS avg_ticket_price
FROM fact_ticket_transactions t
JOIN dim_games g
ON t.game_id=g.game_id
GROUP BY g.opponent
ORDER BY revenue DESC;