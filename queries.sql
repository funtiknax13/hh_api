-- получает список всех компаний и количество вакансий у каждой компании.
SELECT employer_title, vacancies_count FROM (SELECT employer_id, COUNT(*) as vacancies_count
FROM vacancies
GROUP BY employer_id) AS temp_table
RIGHT JOIN employers USING (employer_id)

-- получает список всех вакансий с указанием названия компании,
-- названия вакансии и зарплаты и ссылки на вакансию.
SELECT employer_title, title, GREATEST (salary_from, salary_to) as salary, url
FROM vacancies
JOIN employers USING (employer_id)
ORDER BY salary

-- получает среднюю зарплату по вакансиям.
SELECT ROUND(AVG(salary), 2) FROM
(SELECT GREATEST (salary_from, salary_to) as salary
FROM vacancies) AS test

-- получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
SELECT * FROM vacancies
WHERE GREATEST (salary_from, salary_to) > (SELECT ROUND(AVG(salary), 2) FROM
(SELECT GREATEST (salary_from, salary_to) AS salary
FROM vacancies) AS test)

-- получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”.
SELECT * FROM vacancies
WHERE title LIKE '%Python%'