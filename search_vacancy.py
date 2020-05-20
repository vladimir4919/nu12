#Поиск вакансий на hh.ru

import requests
import pprint
import time
import json

request_text = input('Какую вакансию ищем?:')

# суммарная зарплата по всем вакансиям
salary_total = 0
# общее число найденных вакансий
vacancies_total = 0
# число страниц поиска
NUM_PAGES = 20

key_skills = {}

url = 'https://api.hh.ru/vacancies'

for page_number in range(NUM_PAGES):

    parameters = {
         'text': 'NAME:'+request_text,
         'per_page': 20,
         'page': page_number,
         'only_with_salary': True,

    }

    result = requests.get(url, params=parameters).json()
#    print('Страница:', page_number)
#    pprint.pprint(result)
    # список вакансий
    vacancies = result['items']

    for vacancy in vacancies:
        url_vacancy = vacancy['url']
        # данные по каждой вакансии
        result = requests.get(url_vacancy).json()
        salary = result['salary']

        if salary:

            vacancies_total += 1
            # вычисляем зарплату как среднее между верхним и нижним значением
            salary_start = 0 if salary['from'] is None else salary['from']
            salary_finish = salary_start if salary['to'] is None else salary['to']
            salary_total += (salary_start+salary_finish)/2
            #  ключевые навыки
            skills = result['key_skills']
            for skill in skills:
                item = skill['name']
                if item in key_skills:
                    key_skills[item] += 1
                else:
                    key_skills[item] = 1

            time.sleep(1)

#print(key_skills)

key_skills_sorted = sorted(key_skills.items(), key=lambda x: x[1], reverse=True)
#заносим результаты в словарь
request_result = {}

request_result['request_text'] = request_text
request_result['vacancies_total'] = vacancies_total
request_result['average_salary'] = round(salary_total/vacancies_total,-3)
request_result['key_skills'] = key_skills_sorted

print('ПАРАМЕТРЫ ЗАПРОСА:', request_text)

print('ВСЕГО ВАКАНСИЙ:', vacancies_total)

print('СРЕДНЯЯ ЗАРПЛАТА:', request_result['average_salary'])

print('СПИСОК КЛЮЧЕВЫХ НАВЫКОВ:')
for item in key_skills_sorted:
    print(f'{item[0]} {item[1]}  {round(item[1]/vacancies_total*100)} %' )


#сохранение словаря результатов в файл .json
with open('request_result.json', "w", encoding="utf-8") as file:
    json.dump(request_result, file)

print('Результат сохранен в файле request_result.json')