import yaml
from database import init_db, add_job
from scraper import search_indeed
from matcher import get_similarity

# Load config
with open("config/settings.yaml") as f:
    config = yaml.safe_load(f)

# Load your base resume text (simple example - improve with docx reader later)
with open("data/base_resume.txt", "r", encoding="utf-8") as f:
    resume_text = f.read()

if __name__ == "__main__":
    init_db()
    print("ApplyForge-AI starting...")

    jobs = search_indeed(
        keywords=config['job_search']['keywords'],
        location=config['job_search']['location'],
        pages=config['job_search']['pages_to_search']
    )

    print(f"Found {len(jobs)} jobs. Matching...")

    for job in jobs:
        print(f"\nChecking: {job['title']} at {job['company']}")

        # Placeholder: In real use, fetch full job description from job['link']
        job_desc = "Python developer with experience in automation, NLP, and web scraping."  # Replace with actual fetch

        score = get_similarity(job_desc, resume_text)

        if score >= config['matching']['min_similarity_threshold']:
            print(f"Good match! Score: {score:.2f}")

            job_id = add_job(
                title=job['title'],
                company=job['company'],
                location=config['job_search']['location'],
                job_url=job['link'],
                job_description=job_desc,
                source="Indeed",
                match_score=score
            )
            print(f"Added to database (ID: {job_id})")
        else:
            print(f"Low match: {score:.2f} - skipped")
