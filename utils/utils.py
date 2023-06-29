import psycopg2

from utils.api import HeadHunterAPI


def get_hh_data(employer_ids: list) -> list:
    data = []
    hh = HeadHunterAPI()
    for employer_id in employer_ids:
        employer = hh.get_employer_info(employer_id)
        vacancies = hh.get_employer_vacancies(employer_id, "Python")
        print(len(vacancies))
        data.append({"employer": employer, "vacancies": vacancies})
    return data


def create_database(db_name: str, params: dict):

    conn = psycopg2.connect(dbname="postgres", **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE {db_name}")
    cur.execute(f"CREATE DATABASE {db_name}")

    conn.close()

    conn = psycopg2.connect(dbname=db_name, **params)

    with conn.cursor() as cur:

        cur.execute("""
            CREATE TABLE employers (
                employer_id SERIAL PRIMARY KEY,
                employer_title VARCHAR(255) NOT NULL,
                site_url TEXT,
                hh_url TEXT NOT NULL,
                area VARCHAR(255),
                open_vacancies INTEGER
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                employer_id INT REFERENCES employers(employer_id),
                title VARCHAR NOT NULL,
                salary_from INTEGER,
                salary_to INTEGER,
                salary_currency VARCHAR(10),
                experience VARCHAR,
                url TEXT
            )
        """)

    conn.commit()
    conn.close()


def save_data_to_database(data: list, db_name: str, params: dict):
    """Сохранение данных о работодателях и их вакансиях."""

    conn = psycopg2.connect(dbname=db_name, **params)

    with conn.cursor() as cur:
        for item in data:
            employer_data = item['employer']
            cur.execute(
                """    
                INSERT INTO employers (employer_title, site_url, hh_url, area, open_vacancies)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING employer_id
                """,

                (employer_data["name"], employer_data["site_url"], employer_data["alternate_url"],
                 employer_data["area"]["name"], employer_data["open_vacancies"])
            )
            employer_id = cur.fetchone()[0]
            vacancies_data = item['vacancies']

            for vacancy in vacancies_data:
                if vacancy["salary"]:
                    salary_from = vacancy["salary"]["from"]
                    if not salary_from:
                        salary_from = None
                    salary_to = vacancy["salary"]["to"]
                    if not salary_to:
                        salary_to = None
                    salary_cur = vacancy["salary"]["currency"].lower()
                    if salary_cur == "rur":
                        salary_cur = "rub"
                else:
                    salary_from = None
                    salary_to = None
                    salary_cur = None
                cur.execute(

                    """
                    INSERT INTO vacancies (employer_id, title, salary_from, salary_to, salary_currency, experience, url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (employer_id, vacancy["name"], salary_from, salary_to,
                     salary_cur, vacancy["experience"]["name"], vacancy["url"])
                )

    conn.commit()
    conn.close()
