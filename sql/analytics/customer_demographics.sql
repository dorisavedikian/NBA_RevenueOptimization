SELECT
    age_group,
    income_bracket,
    COUNT(*) AS customers,
    SUM(CASE WHEN season_ticket_holder=1 THEN 1 ELSE 0 END) AS season_ticket_holders
FROM dim_customers
GROUP BY
    age_group,
    income_bracket
ORDER BY
    age_group,
    income_bracket;