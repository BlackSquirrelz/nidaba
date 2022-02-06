SELECT categories.category_name, count(artifacts.ArtifactCategory) as no_artifacts
FROM artifacts
INNER JOIN categories
ON categories.id  = artifacts.ArtifactCategory
GROUP BY categories.category_name
ORDER BY no_artifacts DESC