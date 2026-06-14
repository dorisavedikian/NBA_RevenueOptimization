-- QA checks for NBA Revenue Intelligence

-- 1. Negative revenue
SELECT COUNT(*) AS negative_revenue_rows
FROM fact_ticket_transactions
WHERE revenue < 0;

-- 2. Missing game IDs
SELECT COUNT(*) AS missing_game_ids
FROM fact_ticket_transactions
WHERE game_id IS NULL;

-- 3. Missing customer IDs
SELECT COUNT(*) AS missing_customer_ids
FROM fact_ticket_transactions
WHERE customer_id IS NULL;

-- 4. Games with more tickets sold than capacity
SELECT
    game_id,
    tickets_sold,
    arena_capacity
FROM model_dataset
WHERE tickets_sold > arena_capacity;

-- 5. Invalid sell-through rates
SELECT COUNT(*) AS invalid_sell_through_rows
FROM model_dataset
WHERE sell_through_rate < 0 OR sell_through_rate > 1;