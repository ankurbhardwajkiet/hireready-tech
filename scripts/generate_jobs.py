import json
import uuid
from datetime import datetime, timedelta
import random

today = datetime.now().date()

mass_companies = ["TCS", "Infosys", "Wipro", "HCL", "Tech Mahindra"]
product_companies = ["Zoho", "Flipkart", "Amazon", "Freshworks", "Razorpay"]
intern_companies = ["Microsoft", "Google", "Paytm", "PhonePe", "Swiggy"]

skills_pool = [
    "Python", "Java", "React", "Node.js",
    "SQL", "AWS", "Data Structures",
    "Machine Learning", "Cloud", "Docker"
]

jobs = []

def random_skills():
    return random.sample(skills_pool, 4)

def random_date():
    return str(today - timedelta(days=random.randint(0,5)))

def create_job(company, title, category, exp):
    return {
        "id": str(uuid.uuid4()),
        "title": title,
        "company": company,
        "companyType": category,
        "category": category,
        "location": "India",
        "experience": exp,
        "skills": random_skills(),
        "postedOn": random_date(),
        "status": "Open",
        "applyLink": f"https://careers.{company.lower().replace(' ','')}.com"
    }

for company in mass_companies:
    jobs.append(create_job(company, "Software Engineer", "Mass Recruiter", "0-2 Years"))

for company in product_companies:
    jobs.append(create_job(company, "Backend Developer", "Product Based", "1-3 Years"))

for company in intern_companies:
    jobs.append(create_job(company, "SDE Intern", "Internship", "Internship"))

with open("data/jobs-source.json", "w") as f:
    json.dump(jobs, f, indent=2)

print("Jobs JSON updated successfully.")
