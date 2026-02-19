from scraper.job_scraper import scrape_jobs

role = input("Введите роль для поиска вакансий: ")
pages = input("Сколько страниц нужно запарсить: ")

scrape_jobs(role, pages)