import requests
import json
import time


class HeadHunterAPI:
    """
    Класс для работы с api HeadHunter
    """
    api_vacancies = "https://api.hh.ru/vacancies"
    api_employers = "https://api.hh.ru/employers/"

    def get_employer_vacancies(self, employer_id: int, query: str) -> list:
        """
        Получает список вакансий по ключевому слову name с HH и id работодателя
        """
        data = []
        for page_index in range(30):

            params = {
                'employer_id': employer_id,
                'text': query,
                'page': page_index,
                'per_page': 100
            }
            try:
                response = requests.get(self.api_vacancies, params)
                response_data = json.loads(response.content.decode())["items"]
                data.extend(response_data)
            except Exception as ex:
                break
            time.sleep(3)
        return data

    def get_employer_info(self, employer_id: int) -> dict:
        """
        Возвращает информацию о работодателе с hh
        :param employer_id: id работодателя на hh
        :return: словарь с информацией о работодателе
        """
        response = requests.get(f'{self.api_employers}{employer_id}')
        employer_info = json.loads(response.content.decode())
        return employer_info

    @staticmethod
    def get_all_employers():
        """
        Метод для получения списка всех работодателей на HH
        """
        response = requests.get('https://api.hh.ru/employers')
        employers_count = json.loads(response.content.decode())["found"]
        employers_list = []
        for employer_number in range(1, employers_count):
            response = requests.get('https://api.hh.ru/employers/' + str(employer_number))
            employer_info = json.loads(response.content.decode())
            try:
                employer = {"id": employer_info["id"], "name": employer_info["name"]}
                employers_list.append(employer)
            except KeyError:
                pass
            if employer_number % 200 == 0:
                time.sleep(1)
        with open("employers_list.json", "w", encoding="utf-8") as file:
            json.dump(employers_list, file)
        return employers_list
