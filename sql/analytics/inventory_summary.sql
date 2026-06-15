SELECT
    game_id,
    opponent,
    tickets_sold,
    inventory_remaining,
    ROUND(100*sell_through_rate,2) AS sell_through_pct
FROM model_dataset
ORDER BY sell_through_rate DESC;