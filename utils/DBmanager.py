import psycopg2


class DBmanager:

    def __init__(self, db_name: str, params: dict):
        self.db_name = db_name
        self.params = params

    def get_companies_and_vacancies_count(self):
        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        with conn.cursor() as cur:
            cur.execute("""SELECT employer_title, vacancies_count FROM (SELECT employer_id, COUNT(*) as vacancies_count
                        FROM vacancies
                        GROUP BY employer_id) AS temp_table
                        RIGHT JOIN employers USING (employer_id)""")
            data = cur.fetchall()
            for row in data:
                print(row)
        conn.commit()
        conn.close()

    def get_all_vacancies(self):
        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        with conn.cursor() as cur:
            cur.execute("""SELECT employer_title, title, GREATEST (salary_from, salary_to) as salary, url
                            FROM vacancies
                            JOIN employers USING (employer_id)
                            ORDER BY salary""")
            data = cur.fetchall()
            for row in data:
                print(row)
        conn.commit()
        conn.close()

    def get_avg_salary(self):
        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        with conn.cursor() as cur:
            cur.execute("""SELECT ROUND(AVG(salary), 2) FROM
                            (SELECT GREATEST (salary_from, salary_to) as salary
                            FROM vacancies) AS test""")
            data = cur.fetchall()
            for row in data:
                print(row)
        conn.commit()
        conn.close()

    def get_vacancies_with_higher_salary(self):
        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        with conn.cursor() as cur:
            cur.execute("""SELECT * FROM vacancies
                            WHERE GREATEST (salary_from, salary_to) > (SELECT ROUND(AVG(salary), 2) FROM
                            (SELECT GREATEST (salary_from, salary_to) AS salary
                            FROM vacancies) AS test)""")
            data = cur.fetchall()
            for row in data:
                print(row)
        conn.commit()
        conn.close()

    def get_vacancies_with_keyword(self, keyword: str):
        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        with conn.cursor() as cur:
            cur.execute(f"""SELECT * FROM vacancies
                        WHERE title LIKE '%{keyword}%'""")
            data = cur.fetchall()
            for row in data:
                print(row)
        conn.commit()
        conn.close()
