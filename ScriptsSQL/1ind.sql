-- 1 Задание - Вывести 10 футболистов, которые больше всего голов забивают во втором тайме.

select id, name, top10.second_half_goals
from personal_data
         JOIN (select max_sum.max_goals as second_half_goals, max_sum.person as name_id
               from (select goals_sum.personal_data_id as person, sum(goals_sum.sh_goals) as max_goals
                     from (select personal_data_id, count(event) as sh_goals
                           from match_info
                           where minute > 45
                             and event = 'goal'
                           group by personal_data_id, minute, event
                          ) goals_sum
                     group by goals_sum.personal_data_id) max_sum
               order by max_sum.max_goals DESC
               LIMIT 10) as top10 ON id = top10.name_id
order by top10.second_half_goals DESC;

-- Другой вариант

select personal_data.id, name, count(event) as cnt
from personal_data
         JOIN match_info ON (personal_data.id = personal_data_id and minute > 45 and event = 'goal')
group by personal_data.id, name
order by count(event) DESC LIMIT 10;



select human.first_name, human.second_name from human where human.id = (select reservation.id_human from order
JOIN reservation ON (order.id_reservation = reservation.id) order by count(reservation.id_human)  LIMIT 10)

select teacher.first_name, teacher.second_name, flow_id, group_id, subgroup_id, subject_work_class_id, classroom_id,
       time_start, time_end from schedule join teacher on (schedule.teacher_id = teacher.id and schedule.week_day_num = 1)