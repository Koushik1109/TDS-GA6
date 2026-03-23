WITH thresholds AS (
    SELECT generate_series / 100.0 AS t
    FROM generate_series(5, 95, 5)
),
metrics AS (
    SELECT 
        th.t AS threshold,
        SUM(CASE WHEN p.score >= th.t AND p.true_label = 1 THEN 1 ELSE 0 END) AS tp,
        SUM(CASE WHEN p.score >= th.t AND p.true_label = 0 THEN 1 ELSE 0 END) AS fp,
        SUM(CASE WHEN p.score < th.t AND p.true_label = 1 THEN 1 ELSE 0 END) AS fn,
        COUNT(*) AS total_rows
    FROM thresholds th
    CROSS JOIN predictions p
    GROUP BY th.t
)
SELECT 
    threshold AS optimal_threshold,
    ROUND(tp * 1.0 / NULLIF(tp + fp, 0), 4) AS precision_at_threshold,
    ROUND(tp * 1.0 / NULLIF(tp + fn, 0), 4) AS recall_at_threshold,
    ROUND((10.0 * fn + fp) / total_rows, 6) AS expected_cost_at_threshold
FROM metrics
ORDER BY expected_cost_at_threshold ASC
LIMIT 1;
