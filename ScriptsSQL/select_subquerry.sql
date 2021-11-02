SELECT *
FROM personal_data
WHERE personal_data_id = (SELECT personal_data_id
                          FROM player
                          WHERE player_id = (SELECT player_id
                                             FROM transfer_cost
                                             WHERE season_finish =
                                                   (SELECT max(season_finish) FROM transfer_cost)));