SELECT * from shipping HAVING package_weight > 100
UNION
SELECT * from shipping HAVING package_weight > 1000