SELECT  team.team_ as team, name, match_info.event as event, match_info.minute as minute
FROM personal_data
         JOIN team ON personal_data.team_id = team.team_id
         JOIN match_info ON personal_data.personal_data_id = match_info.personal_data_id
LIMIT 20;
