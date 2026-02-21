from scraper.utils import extract_salary_range

from scraper.utils import extract_salary_range


def parse_job_card(job):
    """
    Parsing one vacancie
    """
    # title
    title = job.find("span", attrs={"data-qa": "serp-item__title-text"})
    title = title.text.strip() if title else "No title"

    # company
    company = job.find(
        "span",
        attrs={"data-qa": "vacancy-serp__vacancy-employer-text"}
    )
    company = company.text.strip() if company else "No company"

    # salary
    salary = "No salary"
    spans = job.find_all("span")

    for s in spans:
        if "₽" in s.text or "$" in s.text or "€" in s.text:
            salary = s.text.strip()
            break

    min_salary, max_salary = extract_salary_range(salary)

    return [title, company, min_salary, max_salary]