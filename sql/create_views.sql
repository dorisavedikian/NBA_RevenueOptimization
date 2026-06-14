DROP VIEW IF EXISTS vw_game_revenue_summary;
DROP VIEW IF EXISTS vw_customer_summary;
DROP VIEW IF EXISTS vw_funnel_summary;
DROP VIEW IF EXISTS vw_executive_dashboard;

CREATE VIEW vw_game_revenue_summary AS
SELECT
    g.game_id,
    g.game_date,
    g.opponent,
    g.day_of_week,
    g.is_weekend,
    g.opponent_strength,
    COUNT(t.transaction_id) AS total_transactions,
    SUM(t.seats_purchased) AS tickets_sold,
    SUM(t.revenue) AS total_revenue,
    AVG(t.ticket_price) AS avg_ticket_price,
    g.arena_capacity,
    g.arena_capacity - SUM(t.seats_purchased) AS inventory_remaining,
    1.0 * SUM(t.seats_purchased) / g.arena_capacity AS sell_through_rate
FROM dim_games g
LEFT JOIN fact_ticket_transactions t
    ON g.game_id = t.game_id
GROUP BY
    g.game_id,
    g.game_date,
    g.opponent,
    g.day_of_week,
    g.is_weekend,
    g.opponent_strength,
    g.arena_capacity;

CREATE VIEW vw_customer_summary AS
SELECT
    c.customer_id,
    c.age_group,
    c.income_bracket,
    c.zip_code,
    c.season_ticket_holder,
    COUNT(t.transaction_id) AS total_transactions,
    COUNT(DISTINCT t.game_id) AS games_attended,
    SUM(t.seats_purchased) AS total_tickets_purchased,
    SUM(t.revenue) AS lifetime_revenue,
    AVG(t.revenue) AS avg_order_value
FROM dim_customers c
LEFT JOIN fact_ticket_transactions t
    ON c.customer_id = t.customer_id
GROUP BY
    c.customer_id,
    c.age_group,
    c.income_bracket,
    c.zip_code,
    c.season_ticket_holder;

CREATE VIEW vw_funnel_summary AS
SELECT
    game_id,
    COUNT(session_id) AS visitors,
    SUM(viewed_ticket_page) AS ticket_page_views,
    SUM(added_to_cart) AS cart_adds,
    SUM(checkout_started) AS checkouts,
    SUM(purchased) AS purchases,
    1.0 * SUM(added_to_cart) / COUNT(session_id) AS cart_rate,
    1.0 * SUM(checkout_started) / NULLIF(SUM(added_to_cart), 0) AS checkout_rate,
    1.0 * SUM(purchased) / COUNT(session_id) AS purchase_rate,
    1.0 - (1.0 * SUM(purchased) / NULLIF(SUM(added_to_cart), 0)) AS cart_abandonment_rate
FROM fact_web_sessions
GROUP BY game_id;

CREATE VIEW vw_executive_dashboard AS
SELECT
    r.game_id,
    r.game_date,
    r.opponent,
    r.day_of_week,
    r.is_weekend,
    r.opponent_strength,
    r.tickets_sold,
    r.total_revenue,
    r.avg_ticket_price,
    r.inventory_remaining,
    r.sell_through_rate,
    f.visitors,
    f.cart_adds,
    f.checkouts,
    f.purchases,
    f.purchase_rate,
    f.cart_abandonment_rate
FROM vw_game_revenue_summary r
LEFT JOIN vw_funnel_summary f
    ON r.game_id = f.game_id;