import requests
from bs4 import BeautifulSoup
import csv
import re


def scrape_jobs(role, pages):
    role_query = role.replace(" ", "+")
    pages_query = int(pages)

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
            title = title.text.strip() if title else "No title"

            company = job.find("span", attrs={"data-qa": "vacancy-serp__vacancy-employer-text"})
            company = company.text.strip() if company else "No company"

            # Salary search at the hh.ru DOM
            salary = "No salary"
            spans = job.find_all("span")
            for s in spans:
                if "₽" in s.text or "$" in s.text or "€" in s.text:
                    salary = s.text.strip()
                    break

            def salary_min_max(salary):
                if not salary or salary == "No salary":
                    return None, None
                
                salary = salary.replace(" ", "").replace("\xa0", "").replace("\u202f", "")
                salary_nums = re.findall(r"\d+", salary) # Getting all the numbers from the text using RegExp
                salary_nums = [int(i) for i in salary_nums] # Making all the ddigits integers because the are saving as a string

                if len(salary_nums) == 1:
                    return salary_nums[0], salary_nums[0]
                elif len(salary_nums) >= 2:
                    return salary_nums[0], salary_nums[1]
                
                return None, None
            
            min_salary, max_salary = salary_min_max(salary)

            all_jobs.append([title, company, min_salary, max_salary])

    # запись CSV
    with open("jobs.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "Company", "Minimum Salary in ₽", "Maximum Salary in ₽"])
        writer.writerows(all_jobs)

    print(f"Сохранено {len(all_jobs)} вакансий")