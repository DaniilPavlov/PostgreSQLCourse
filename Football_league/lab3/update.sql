SELECT *
FROM transfer_cost
WHERE season_finish > 120000000;

UPDATE transfer_cost
SET season_finish = 140000000
WHERE season_finish > 120000000;

SELECT *
FROM transfer_cost
WHERE season_finish > 120000000;