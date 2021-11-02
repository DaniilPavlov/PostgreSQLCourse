SELECT *
FROM transfer_cost
WHERE player_id IN (SELECT player_id
                    FROM player
                    WHERE personal_data_id IN (SELECT personal_data_id
                                               FROM personal_data
                                               WHERE weight > 89));

DELETE
FROM transfer_cost
WHERE player_id IN (SELECT player_id
                    FROM player
                    WHERE personal_data_id IN (SELECT personal_data_id
                                               FROM personal_data
                                               WHERE weight > 80));

SELECT *
FROM transfer_cost
WHERE player_id IN (SELECT player_id
                    FROM player
                    WHERE personal_data_id IN (SELECT personal_data_id
                                               FROM personal_data
                                               WHERE weight > 89));
