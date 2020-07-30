SELECT * from shipping HAVING package_weight > 100
UNION ALL
SELECT * from shipping HAVING package_weight > 1000