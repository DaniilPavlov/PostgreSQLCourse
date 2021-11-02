-- 2 Задание - Вывести 5 футболистов, которых реже всего заменяют.

select id, name, top5.substitutions
from personal_data
         JOIN (select max_sum.max_subs as substitutions, max_sum.person as name_id
               from (select subs_sum.personal_data_id as person, sum(subs_sum.subs) as max_subs
                     from (select personal_data_id, count(event) as subs
                           from match_info
                           where event = 'replaced'
                           group by personal_data_id, event) subs_sum
                     group by subs_sum.personal_data_id) max_sum
               order by max_sum.max_subs
               LIMIT 5) as top5 ON id = top5.name_id
order by top5.substitutions;

-- Другой вариант

select personal_data.id, name, count(event) as cnt
from personal_data
         JOIN match_info ON (personal_data.id = personal_data_id and event = 'replaced')
group by personal_data.id
order by count(event) LIMIT 5