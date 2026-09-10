-- SQL Business Analysis Portfolio Project
-- Denae Camacho
--
-- This file contains three BigQuery analyses demonstrating CTEs, joins,
-- correlated subqueries, filtering, aggregation, grouping, and sorting.

-- ============================================================
-- 1. Austin Bikeshare: Station most used by the longest-used bike
-- ============================================================

WITH longest_used_bike AS (
    SELECT
        bike_id,
        SUM(duration_minutes) AS total_trip_duration
    FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips`
    GROUP BY bike_id
    ORDER BY total_trip_duration DESC
    LIMIT 1
)

SELECT
    trips.start_station_id,
    COUNT(*) AS trip_count
FROM longest_used_bike AS longest
INNER JOIN `bigquery-public-data.austin_bikeshare.bikeshare_trips` AS trips
    ON longest.bike_id = trips.bike_id
GROUP BY trips.start_station_id
ORDER BY trip_count DESC
LIMIT 1;


-- ============================================================
-- 2. NYC Citi Bike: Trips farthest above station average
-- ============================================================

SELECT
    starttime,
    start_station_id,
    tripduration,
    (
        SELECT ROUND(AVG(tripduration), 2)
        FROM `bigquery-public-data.new_york_citibike.citibike_trips`
        WHERE start_station_id = outer_trips.start_station_id
    ) AS avg_duration_for_station,
    ROUND(
        tripduration - (
            SELECT AVG(tripduration)
            FROM `bigquery-public-data.new_york_citibike.citibike_trips`
            WHERE start_station_id = outer_trips.start_station_id
        ),
        2
    ) AS difference_from_avg
FROM `bigquery-public-data.new_york_citibike.citibike_trips` AS outer_trips
ORDER BY difference_from_avg DESC
LIMIT 25;


-- ============================================================
-- 3. Wikipedia: Google-related article views by language
-- ============================================================

SELECT
    language,
    title,
    SUM(views) AS total_views
FROM `bigquery-samples.wikipedia_benchmark.Wiki10B`
WHERE title LIKE '%Google%'
GROUP BY
    language,
    title
ORDER BY total_views DESC;
