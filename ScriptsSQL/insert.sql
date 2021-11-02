INSERT INTO league
VALUES (5, 'Tinkoff');

INSERT INTO team
VALUES (81, 5, 'Lokomotiv'),
       (82, 5, 'Zenit');

INSERT INTO personal_data
VALUES (881, 81, 'ANTON MIRANCHUK', '1997-06-05', 'Russia', 70, 176),
       (882, 81, 'MARINATO GUILHERME', '1992-08-17', 'Brazil', 77, 189),
       (883, 82, 'YURII ZHIRKOV', '1986-02-21', 'Russia', 70, 173),
       (884, 82, 'ANTON ZABALOTNIY', '1993-05-09', 'Russia', 75, 179);

INSERT INTO contract
VALUES (881, 881, 100000, '2018-08-19', '2022-08-19'),
       (882, 882, 110000, '2016-07-11', '2021-08-08'),
       (883, 883, 80000, '2019-06-22', '2021-06-25'),
       (884, 884, 55000, '2017-06-07', '2021-06-01');

INSERT INTO player
VALUES (3521, 881, 'LM', '2016-2017'),
       (3522, 881, 'RM', '2017-2018'),
       (3523, 881, 'CM', '2018-2019'),
       (3524, 881, 'LM', '2019-2020'),

       (3525, 882, 'GK', '2016-2017'),
       (3526, 882, 'GK', '2017-2018'),
       (3527, 882, 'GK', '2018-2019'),
       (3528, 882, 'GK', '2019-2020'),

       (3529, 883, 'LM', '2016-2017'),
       (3530, 883, 'LB', '2017-2018'),
       (3531, 883, 'LM', '2018-2019'),
       (3532, 883, 'RB', '2019-2020'),

       (3533, 884, 'LM', '2016-2017'),
       (3534, 884, 'ST', '2017-2018'),
       (3535, 884, 'ST', '2018-2019'),
       (3536, 884, 'ST', '2019-2020');



INSERT INTO transfer_cost
VALUES (3521, 3521, 1000000, 2000000),
       (3522, 3522, 2500000, 4000000),
       (3523, 3523, 10000000, 18000000),
       (3524, 3524, 18000000, 29000000),

       (3525, 3525, 10000000, 10000000),
       (3526, 3526, 9000000, 7000000),
       (3527, 3527, 6500000, 8000000),
       (3528, 3528, 5000000, 3000000),

       (3529, 3529, 4000000, 4000000),
       (3530, 3530, 3000000, 3000000),
       (3531, 3531, 3000000, 3000000),
       (3532, 3532, 1000000, 800000),

       (3533, 3533, 11000000, 12000000),
       (3534, 3534, 11000000, 9000000),
       (3535, 3535, 8000000, 7000000),
       (3536, 3536, 7000000, 7000000);

INSERT INTO match
VALUES (6081, 81, 82, '2-0', '2020-05-22');

INSERT INTO match_info
VALUES (48697, 6081, 881, 76, 'goal'),
       (48698, 6081, 881, 89, 'goal');

INSERT INTO users (login,password,user_status)
VALUES ('a',crypt('123', gen_salt('bf')),'user'),('b',crypt('456', gen_salt('bf')),'admin'),
       ('c',crypt('789', gen_salt('bf')),'user'),('d',crypt('123', gen_salt('bf')),'admin');

INSERT INTO users (login,password,user_status)
VALUES ('a','123','user'),('b','456','admin');

SELECT id, login FROM users WHERE login = 'a'
   AND password = crypt('123', password);

update users set password = crypt(password,gen_salt('bf'));

INSERT into personal_data (team_id, name, birthday, nationality, weight, height) VALUES ('1','VASILIY MAKSEM', '10-10-1999','Russia', 73,173);

INSERT INTO player (personal_data_id, position, season_id) VALUES ('50','ST',2) IF NOT EXISTS  ;