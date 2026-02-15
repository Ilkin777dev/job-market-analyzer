import requests
from bs4 import BeautifulSoup
import csv


def scrape_jobs(role):
    """
    Минимальный пример парсера вакансий по роли.
    """
    # заменяем пробелы на + для URL
    role_query = role.replace(" ", "+")

    # тестовый URL (позже заменим на реальный сайт)
    url = f"https://hh.ru/search/vacancy?text={role_query}"

    # Создаем нашего User Агента чтобы проходить блокировку и получать нужную страницу при запросе
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36"}    

    # отправляем HTTP запрос
    response = requests.get(url, headers = headers)
    print(response.text)

    # проверяем успешность запроса
    if response.status_code != 200:
        print("Ошибка запроса:", response.status_code)
        return

    # превращаем HTML текст в объект BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # ищем вакансии (пример структуры сайта)
    jobs = soup.find_all("a", attrs={"data-qa": "serp-item__title"})
    print("Found jobs:", len(jobs))

    # записываем данные в CSV
    with open("jobs.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "Description"])

        for job in jobs:
            title = job.text.strip()
            writer.writerow([title, ""])
            # desc = job.find("p").text.strip()
            # writer.writerow([title, desc])

    print(f"Найдено {len(jobs)} вакансий. Данные сохранены в jobs.csv")