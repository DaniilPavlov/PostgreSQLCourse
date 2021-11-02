SELECT *
FROM match_info
WHERE minute = (SELECT MAX(minute) FROM match_info);

DELETE
FROM match_info
WHERE minute = (SELECT MAX(minute) FROM match_info);

SELECT *
FROM match_info
WHERE minute = (SELECT MAX(minute) FROM match_info);