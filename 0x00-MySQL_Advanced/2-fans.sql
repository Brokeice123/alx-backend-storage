-- Script that ranks country origins of bands
-- Order is by number of fans
-- Column names must be: origin and nb_fans

SELECT origin, SUM(fans) AS nb_fans
FROM metal_bands
GROUP BY origin
ORDER BY nb_fans DESC