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
    # print(response.text)

    # проверяем успешность запроса
    if response.status_code != 200:
        print("Ошибка запроса:", response.status_code)
        return

    # превращаем HTML текст в объект BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # ищем вакансии (пример структуры сайта)
    jobs = soup.find_all("div", attrs={"data-qa": "vacancy-serp__vacancy"})
    # print("Found jobs:", len(jobs))

    # записываем данные в CSV
    with open("jobs.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "Salary", "Company"])

        for job in jobs:
            title = job.find("span", attrs={"data-qa": "serp-item__title-text"})
            title = title.text.strip() if title else "None"

            salary = "No salary"
            for span in job.find_all("span"):
                text = span.get_text()
                if "₽" in text or "$" in text or "₼" in text:
                    salary = text.strip()
                    break

            company = job.find("span", attrs={"data-qa": "vacancy-serp__vacancy-employer-text"})
            company = company.text.strip() if company else "None"

            writer.writerow([title, salary, company])

            # title = job.text.strip()
            # sallary = job.text
            # writer.writerow([title, ""])
            # desc = job.find("p").text.strip()
            # writer.writerow([title, desc])

    print(f"Найдено {len(jobs)} вакансий. Данные сохранены в jobs.csv")