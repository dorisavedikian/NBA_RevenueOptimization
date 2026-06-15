SELECT
    g.opponent,
    ROUND(AVG(ticket_price),2) AS average_price,
    SUM(revenue) AS revenue,
    SUM(seats_purchased) AS tickets
FROM fact_ticket_transactions t
JOIN dim_games g
ON t.game_id=g.game_id
GROUP BY g.opponent
ORDER BY average_price DESC;