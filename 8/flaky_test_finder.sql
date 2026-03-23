WITH commit_aggregates AS (
    SELECT 
        test_name,
        commit_hash,
        COUNT(*) AS runs_on_commit,
        COUNT(*) FILTER (WHERE outcome = 'PASS') AS passes_on_commit,
        COUNT(*) FILTER (WHERE outcome = 'FAIL') AS fails_on_commit
    FROM test_runs
    GROUP BY test_name, commit_hash
),
test_aggregates AS (
    SELECT 
        test_name,
        CAST(SUM(CASE WHEN passes_on_commit > 0 AND fails_on_commit > 0 THEN 1 ELSE 0 END) AS INTEGER) AS flaky_commits,
        COUNT(commit_hash) AS total_commits,
        SUM(passes_on_commit) AS total_passes,
        SUM(runs_on_commit) AS total_runs
    FROM commit_aggregates
    GROUP BY test_name
)
SELECT 
    test_name,
    flaky_commits,
    CAST(ROUND(CAST(total_passes AS DOUBLE) / total_runs, 4) AS FLOAT) AS pass_rate,
    CAST(ROUND(CAST(flaky_commits AS DOUBLE) / total_commits, 4) AS FLOAT) AS flakyness_score
FROM test_aggregates
WHERE flaky_commits > 0
ORDER BY flakyness_score DESC;
