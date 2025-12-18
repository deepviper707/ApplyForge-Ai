import yaml
from database import init_db, add_job
from scraper import search_indeed
from matcher import get_similarity

with open("config/settings.yaml") as f:
    config = yaml.safe_load(f)

# Load resume text
with open("data/base_resume.txt", "r", encoding="utf-8") as f:
    resume_text = f.read()

if __name__ == "__main__":
    init_db()
    print("ApplyForge-AI: Searching and fetching full descriptions...")

    jobs = search_indeed(
        keywords=config['job_search']['keywords'],
        location=config['job_search']['location'],
        pages=config['job_search']['pages_to_search']
    )

    print(f"Found and processed {len(jobs)} jobs.\n")

    for job in jobs:
        print(f"Matching: {job['title']} at {job['company']}")
        
        score = get_similarity(job['description'], resume_text)
        
        if score >= config['matching']['min_similarity_threshold']:
            print(f"Strong match: {score:.2f}")
            add_job(
                title=job['title'],
                company=job['company'],
                location=config['job_search']['location'],
                salary="",  # Add salary parsing later
                job_url=job['link'],
                job_description=job['description'],
                source="Indeed",
                match_score=score
            )
        else:
            print(f"Skip: {score:.2f}")
