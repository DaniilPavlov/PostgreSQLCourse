SELECT MAX(match_id), personal_data_id, COUNT(event), AVG(minute)
FROM match_info
GROUP BY personal_data_id
HAVING personal_data_id < 12;