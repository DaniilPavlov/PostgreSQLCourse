SELECT count(minute) as first_half_goals
FROM match_info
WHERE minute BETWEEN 1 and 45;