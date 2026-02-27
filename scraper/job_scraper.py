import time
import random
import requests
from bs4 import BeautifulSoup
import csv
import re
from database.db_manager import create_table, insert_all_jobs
from scraper.utils import extract_salary_range
from scraper.parser import parse_job_card
from scraper.filters import filter_by_min_salary


def scrape_jobs(role, pages, min_salary=None):
    role_query = role.replace(" ", "+")
    pages_query = int(pages)

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    all_jobs = []

    # looping pages
    for page in range(pages_query):
        print(f"Parsing page № {page+1}...")

        url = f"https://hh.ru/search/vacancy?text={role_query}&page={page}"
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print("Request error:", response.status_code)
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        jobs = soup.find_all("div", attrs={"data-qa": "vacancy-serp__vacancy"})

        for job in jobs:
            job_data = parse_job_card(job) # Using parse_job_card from parser
            if min_salary:
               if not filter_by_min_salary(job_data, min_salary):
                continue 
            all_jobs.append(job_data)
        
        time.sleep(random.uniform(1,3))

    # запись CSV
    with open("jobs.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "Company", "Minimum Salary in ₽", "Maximum Salary in ₽", "Location", "Link"])
        # writer.writerows(all_jobs)
        for i in all_jobs:
            writer.writerow([
                i["title"],
                i["company"],
                i["min_salary"],
                i["max_salary"],
                i["location"],
                i["link"]
            ])

    # Adding data from all_jobes variable into the db
    create_table()
    insert_all_jobs(all_jobs)
    print(f"Saved: {len(all_jobs)} vacancies into jobs.csv, also added all the data to the DB")