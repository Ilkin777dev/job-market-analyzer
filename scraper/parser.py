from scraper.utils import extract_salary_range

def parse_job_card(job):
    """
    Parsing one vacancie
    """
    # title
    title = job.find("span", attrs={"data-qa": "serp-item__title-text"})
    title = title.text.strip() if title else "No title"

    # company
    company = job.find("span",attrs={"data-qa": "vacancy-serp__vacancy-employer-text"})
    company = company.text.strip() if company else "No company"

    # location
    location = job.find(attrs={"data-qa": "vacancy-serp__vacancy-address"})
    location = location.text.strip() if location else "No location"

    # link
    link_tag = job.find("a", attrs={"data-qa": "serp-item__title"})
    link = link_tag['href'] if link_tag else "No link"

    # salary
    salary = "No salary"
    spans = job.find_all("span")

    for s in spans:
        if "₽" in s.text or "$" in s.text or "€" in s.text:
            salary = s.text.strip()
            break

    min_salary, max_salary = extract_salary_range(salary) # Using salary range from utils

    # return [title, company, min_salary, max_salary]
    return {
        "title": title,
        "company": company,
        "min_salary": min_salary,
        "max_salary": max_salary,
        "location": location,
        "link": link
    }