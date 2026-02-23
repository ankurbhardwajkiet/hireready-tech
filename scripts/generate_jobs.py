import json
import uuid
import random
from datetime import datetime, timedelta
import os

DATA_FILE = "data/jobs-source.json"

today = datetime.now().date()

# ---------- CONFIG ----------
MASS_RECRUITER_AGE = 25       # Mass Recruiter close after 25 days
OTHER_JOB_AGE = 20            # Product + Internship close after 20 days
CLOSED_RETENTION_DAYS = 7     # Remove closed jobs after 7 days
NEW_JOBS_PER_CATEGORY = 3
# ----------------------------

mass_companies = ["TCS", "Infosys", "Wipro", "HCL", "Tech Mahindra"]
product_companies = ["Zoho", "Flipkart", "Amazon", "Freshworks", "Razorpay"]
intern_companies = ["Microsoft", "Google", "Paytm", "PhonePe", "Swiggy"]

locations = ["India", "Bangalore", "Hyderabad", "Remote", "Chennai"]

skills_pool = [
    "Python", "Java", "React", "Node.js",
    "SQL", "AWS", "Data Structures",
    "Machine Learning", "Cloud", "Docker"
]

# ---------- HELPERS ----------

def random_skills():
    return random.sample(skills_pool, 4)

def random_location():
    return random.choice(locations)

def generate_job(company, title, category, exp):
    return {
        "id": str(uuid.uuid4()),
        "title": title,
        "company": company,
        "companyType": category,
        "category": category,
        "location": random_location(),
        "experience": exp,
        "skills": random_skills(),
        "postedOn": str(today),
        "status": "Open",
        "applyLink": f"https://careers.{company.lower().replace(' ','')}.com"
    }

def load_existing_jobs():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_jobs(jobs):
    with open(DATA_FILE, "w") as f:
        json.dump(jobs, f, indent=2)

def is_duplicate(existing_jobs, new_job):
    for job in existing_jobs:
        if job["title"] == new_job["title"] and job["company"] == new_job["company"]:
            return True
    return False

# ---------- LOAD EXISTING ----------
jobs = load_existing_jobs()
updated_jobs = []

# ---------- CLEAN OLD JOBS ----------
for job in jobs:
    posted_date = datetime.strptime(job["postedOn"], "%Y-%m-%d").date()
    age = (today - posted_date).days

    # Auto close logic
    if job["status"] == "Open":
        if job["category"] == "Mass Recruiter" and age > MASS_RECRUITER_AGE:
            job["status"] = "Closed"
            job["closedOn"] = str(today)
        elif job["category"] != "Mass Recruiter" and age > OTHER_JOB_AGE:
            job["status"] = "Closed"
            job["closedOn"] = str(today)

    # Remove closed jobs after retention period
    if job["status"] == "Closed":
        closed_date = datetime.strptime(
            job.get("closedOn", job["postedOn"]), "%Y-%m-%d"
        ).date()
        if (today - closed_date).days > CLOSED_RETENTION_DAYS:
            continue

    updated_jobs.append(job)

# ---------- GENERATE NEW JOBS ----------
for _ in range(NEW_JOBS_PER_CATEGORY):

    mass = random.choice(mass_companies)
    prod = random.choice(product_companies)
    intern = random.choice(intern_companies)

    new_jobs = [
        generate_job(mass, "Software Engineer", "Mass Recruiter", "0-2 Years"),
        generate_job(prod, "Backend Developer", "Product Based", "1-3 Years"),
        generate_job(intern, "SDE Intern", "Internship", "Internship")
    ]

    for new_job in new_jobs:
        if not is_duplicate(updated_jobs, new_job):
            updated_jobs.append(new_job)

# ---------- SORT NEWEST FIRST ----------
updated_jobs.sort(
    key=lambda x: datetime.strptime(x["postedOn"], "%Y-%m-%d"),
    reverse=True
)

# ---------- SAVE ----------
save_jobs(updated_jobs)

print("Persistent job engine executed successfully.")
