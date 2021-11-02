SELECT *
FROM personal_data
WHERE nationality LIKE 'Italy'
  and team_id IN (SELECT team_id
                  FROM team
                  WHERE league_id IN (1, 4))
  and birthday BETWEEN '1995-12-01' and '2000-01-01';