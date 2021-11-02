SELECT *
FROM match_info
WHERE minute = (SELECT MAX(minute) FROM match_info);

DELETE
FROM match_info
WHERE minute = (SELECT MAX(minute) FROM match_info);

SELECT *
FROM match_info;

DELETE FROM personal_data where id >= 2804;

DELETE FROM match where id >18620;

DELETE FROM player where id >=21194