import psycopg2


class DBmanager:

    def __init__(self, db_name: str, params: dict):
        self.db_name = db_name
        self.params = params

    def get_companies_and_vacancies_count(self):
        """
        Вывод списка всех компаний и количество их вакансий
        :return: None
        """
        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        with conn.cursor() as cur:
            cur.execute("""SELECT employer_title, vacancies_count FROM (SELECT employer_id, COUNT(*) as vacancies_count
                        FROM vacancies
                        GROUP BY employer_id) AS temp_table
                        RIGHT JOIN employers USING (employer_id)""")
            data = cur.fetchall()
            self.print_data(data)
        conn.commit()
        conn.close()

    def get_all_vacancies(self):
        """
        Вывод списка всех вакансий
        :return: None
        """
        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        with conn.cursor() as cur:
            cur.execute("""SELECT employer_title, title, GREATEST (salary_from, salary_to) as salary, url
                            FROM vacancies
                            JOIN employers USING (employer_id)
                            ORDER BY salary""")
            data = cur.fetchall()
            self.print_data(data)
        conn.commit()
        conn.close()

    def get_avg_salary(self):
        """
        Вывод средней зарплаты всех вакансий
        :return: None
        """
        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        with conn.cursor() as cur:
            cur.execute("""SELECT ROUND(AVG(salary), 2) FROM
                            (SELECT GREATEST (salary_from, salary_to) as salary
                            FROM vacancies) AS test""")
            data = cur.fetchall()
            self.print_data(data)
        conn.commit()
        conn.close()

    def get_vacancies_with_higher_salary(self):
        """
        Вывод списка вакнсий, у которых ЗП выше средней
        :return: None
        """
        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        with conn.cursor() as cur:
            cur.execute("""SELECT * FROM vacancies
                            WHERE GREATEST (salary_from, salary_to) > (SELECT ROUND(AVG(salary), 2) FROM
                            (SELECT GREATEST (salary_from, salary_to) AS salary
                            FROM vacancies) AS test)""")
            data = cur.fetchall()
            self.print_data(data)
        conn.commit()
        conn.close()

    def get_vacancies_with_keyword(self, keyword: str):
        """
        Вывод списка вакансий по ключевому слову
        :param keyword: Ключевое слово
        :return:
        """
        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        with conn.cursor() as cur:
            cur.execute(f"""SELECT * FROM vacancies
                        WHERE title LIKE '%{keyword}%'""")
            data = cur.fetchall()
            self.print_data(data)
        conn.commit()
        conn.close()

    @staticmethod
    def print_data(data):
        """
        Вывод данных полученных после запроса из БД
        :param data: данные запроса
        :return: none
        """
        for item in data:
            for column in item:
                print(column, end="\t")
            print()

