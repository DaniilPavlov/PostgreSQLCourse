SELECT count(event) as number_one_goals
FROM match_info
WHERE event LIKE 'goal' and personal_data_id = 1;