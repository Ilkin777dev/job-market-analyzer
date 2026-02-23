def filter_by_min_salary(job, min_salary):
    job_min_salary = job["min_salary"]

    if job_min_salary is None:
        return False
    
    return job_min_salary >= min_salary