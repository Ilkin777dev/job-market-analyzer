import requests
from bs4 import BeautifulSoup
import csv
import re
from scraper.utils import extract_salary_range
from scraper.parser import parse_job_card


def scrape_jobs(role, pages):
    role_query = role.replace(" ", "+")
    pages_query = int(pages)

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    all_jobs = []

    # looping pages
    for page in range(pages_query):
        print(f"Парсим страницу {page+1}...")

        url = f"https://hh.ru/search/vacancy?text={role_query}&page={page}"
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print("Ошибка запроса:", response.status_code)
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        jobs = soup.find_all("div", attrs={"data-qa": "vacancy-serp__vacancy"})

        for job in jobs:
            job_data = parse_job_card(job) # Using parse_job_card from parser
            all_jobs.append(job_data)

    # запись CSV
    with open("jobs.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "Company", "Minimum Salary in ₽", "Maximum Salary in ₽"])
        writer.writerows(all_jobs)

    print(f"Сохранено {len(all_jobs)} вакансий")