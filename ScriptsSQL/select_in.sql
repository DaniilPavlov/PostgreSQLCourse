SELECT COUNT(*)
FROM match_info
WHERE match_id IN (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
  AND  personal_data_id IN (1, 12, 23, 34, 45, 56, 67, 78, 89, 100);