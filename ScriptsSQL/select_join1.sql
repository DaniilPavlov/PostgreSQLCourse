SELECT name, birthday, nationality, team.team_ as team
FROM personal_data
         JOIN team ON personal_data.team_id = team.team_id
LIMIT 11;
