SELECT COUNT(nationality) AS from_yemen,
       AVG(weight)        AS avg_weight,
       MAX(height)        AS max_height
FROM personal_data
WHERE nationality LIKE 'Yemen'
  and birthday IN ('1990-02-02', '1994-05-10', '1996-01-07');