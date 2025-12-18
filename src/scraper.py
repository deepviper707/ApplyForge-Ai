import requests
from bs4 import BeautifulSoup
import json
import time
import random

def fetch_linkedin_job_description(job_url):
    """Fetch full job description from LinkedIn job page using ld+json."""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        response = requests.get(job_url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        script = soup.find('script', type='application/ld+json')
        if script:
            data = json.loads(script.string)
            return data.get('description', 'No description found').strip()
        return "No ld+json found."
    except Exception as e:
        return f"Error: {str(e)}"

def search_linkedin(keywords, location="United States", pages=2):
    jobs = []
    for start in range(0, pages * 25, 25):  # LinkedIn: 25 jobs per page
        url = f"https://www.linkedin.com/jobs/search/?keywords={keywords.replace(' ', '%20')}&location={location.replace(' ', '%20')}&start={start}&sortBy=DD"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Blocked or error: {response.status_code}")
            break
        soup = BeautifulSoup(response.text, 'html.parser')
        listings = soup.find_all('div', class_='base-card')  # Common job card class
        for card in listings:
            link_tag = card.find('a')
            if not link_tag:
                continue
            job_url = link_tag['href'].split('?')[0]
            title = card.find('h3') or card.find('span', title=True)
            title = title.get_text(strip=True) if title else "Unknown"
            company = card.find('h4') or card.find('a', {'data-tracking-control-name': 'public_jobs_jserp-result_company-name'})
            company = company.get_text(strip=True) if company else "Unknown"
            
            time.sleep(random.uniform(2, 5))  # Delay to avoid blocks
            description = fetch_linkedin_job_description(job_url)
            
            jobs.append({
                "title": title,
                "company": company,
                "link": job_url,
                "description": description
            })
    return jobs
