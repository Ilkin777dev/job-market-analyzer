from scraper.job_scraper import scrape_jobs

role = input("Введите роль для поиска вакансий: ")
pages = input("Сколько страниц нужно запарсить: ")
min_salary = input("Введите минимальную зарплату: ")

min_salary = int(min_salary) if min_salary else None

scrape_jobs(role, pages, min_salary)