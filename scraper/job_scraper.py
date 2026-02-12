import requests
from bs4 import BeautifulSoup
import csv

def scrape_jobs(role):
    """
    Минимальный пример парсера вакансий.
    """
    role_query = role.replace(" ", "+")
    # Тестовый URL, заменим на реальный сайт позже
    url = f"https://hh.ru/jobs?q={role_query}"

    response = requests.get(url)
    if response.status_code != 200:
        print("Ошибка запроса:", response.status_code)
        return

    soup = BeautifulSoup(response.text, "html.parser")
    jobs = soup.find_all("div", class_="job-card")  # пример HTML структуры

    with open("jobs.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "Description"])
        for job in jobs:
            title = job.find("h2").text.strip()
            desc = job.find("p").text.strip()
            writer.writerow([title, desc])

    print(f"Найдено {len(jobs)} вакансий. Данные сохранены в jobs.csv")