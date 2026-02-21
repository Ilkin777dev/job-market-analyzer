import re

def extract_salary_range(salary_text):
    if not salary_text or salary_text == "No salary":
        return None, None

    salary_text = salary_text.replace("\u202f", "").replace("\u202f", "").replace(" ", "")

    salary_nums = re.findall(r"\d+", salary_text)
    salary_nums = [int(i) for i in salary_nums]

    if len(salary_nums) == 1:
        return salary_nums[0], salary_nums[0]

    if len(salary_nums) >= 2:
        return salary_nums[0], salary_nums[1]

    return None, None