from utils.DBmanager import DBmanager
from utils.utils import *
from utils.config import config


def user_interaction():
    """
    Функция взаимодействия с пользователем
    """
    # Список выбранных работодателей (id с HeadHunter)
    employer_ids = [3529, 1740, 80, 78638, 3809, 4219, 3776, 23186, 59, 988387]

    params = config()
    while True:
        print("1 - Создать базу данных, 2 - Вывести данные, 3 - Выход.")
        user_choice = input("Выберите действие (введите цифру меню): ")
        if user_choice == "1":
            create_database("hh_api", params)
            data = get_hh_data(employer_ids)
            save_data_to_database(data, "hh_api", params)
            print("База данных создана и заполнена")
        elif user_choice == "2":
            db_connect = DBmanager("hh_api", params)
            while True:
                print("\n1 - Вывести количество вакансий по компаниям", "2 - Вывести все вакансии",
                      "3 - Вывести среднюю зарплату по вакансиям", "4 - Вывести вакансии с зарплатой выше средней",
                      "5 - Вывести вакансии по ключевому слову", "6 - Вернуться в главное меню", sep="\n")
                user_choice_2 = input("Выберите действие (введите цифру меню): ")
                if user_choice_2 == "1":
                    db_connect.get_companies_and_vacancies_count()
                elif user_choice_2 == "2":
                    db_connect.get_all_vacancies()
                elif user_choice_2 == "3":
                    db_connect.get_avg_salary()
                elif user_choice_2 == "4":
                    db_connect.get_vacancies_with_higher_salary()
                elif user_choice_2 == "5":
                    user_keyword = input("Введите ключевое слово для поиска: ")
                    db_connect.get_vacancies_with_keyword(user_keyword)
                else:
                    break
        else:
            print("Программа завершена")
            break


if __name__ == '__main__':
    user_interaction()
