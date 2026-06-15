SELECT
    game_date,
    opponent,
    tickets_sold,
    total_revenue,
    avg_ticket_price,
    sell_through_rate,
    inventory_remaining,
    predicted_revenue,
    sellout_probability
FROM revenue_forecasts
ORDER BY game_date;