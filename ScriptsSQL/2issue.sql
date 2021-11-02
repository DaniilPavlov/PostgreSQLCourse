SELECT people.first_name, people.last_name FROM attempt INNER JOIN people ON people.id = attempt.athlete
WHERE discipline_id=число AND (competition_id=число или competition_id=число)

select last_name, frist_name, competition.year from people left join attempt on attempt.id = people.id
left join concurrency_attempt on attempt.concurrency_attempt_id = concurrency_attempt.id
left join discipline on concurrency_attempt.discipline_id = discipline.id
left join competition on concurrency_attempt.competition_id = competition.id
where discipline.name = "sport name" group by competition.year order by attempt.result DESC;