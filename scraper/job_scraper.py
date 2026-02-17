import requests
from bs4 import BeautifulSoup
import csv


def scrape_jobs(role, pages):
    role_query = role.replace(" ", "+")
    pages_query = int(pages.replace(" ", "+"))

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    all_jobs = []

    # цикл по страницам
    for page in range(pages_query):
        print(f"Парсим страницу {page+1}...")

        url = f"https://hh.ru/search/vacancy?text={role_query}&page={page}"
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print("Ошибка запроса:", response.status_code)
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        jobs = soup.find_all("div", attrs={"data-qa": "vacancy-serp__vacancy"})
        print("Found jobs:", len(jobs))

        for job in jobs:
            title = job.find("span", attrs={"data-qa": "serp-item__title-text"})
            # data-qa="serp-item__title-text" Vacancies titles data-qa
            title = title.text.strip() if title else "No title"

            company = job.find("span", attrs={"data-qa": "vacancy-serp__vacancy-employer-text"})
            company = company.text.strip() if company else "No company"

            # поиск зарплаты
            salary = "No salary"
            spans = job.find_all("span")
            for s in spans:
                if "₽" in s.text or "$" in s.text or "€" in s.text:
                    salary = s.text.strip()
                    break

            all_jobs.append([title, company, salary])

    # запись CSV
    with open("jobs.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "Company", "Salary"])
        writer.writerows(all_jobs)

    print(f"Сохранено {len(all_jobs)} вакансий")