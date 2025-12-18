import requests
from bs4 import BeautifulSoup
import time
import random

def fetch_job_description(job_link):
    """Fetch full job description from Indeed job page."""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        response = requests.get(job_link, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Indeed job description selector (update if changes)
        desc_div = soup.find('div', {'id': 'jobDescriptionText'}) or soup.find('div', class_='jobsearch-jobDescriptionText')
        if desc_div:
            return desc_div.get_text(strip=True, separator='\n')
        return "Description not found."
    except Exception as e:
        return f"Error fetching: {str(e)}"

def search_indeed(keywords, location="United States", pages=2):
    jobs = []
    base_url = "https://www.indeed.com/jobs"
    for p in range(pages):
        params = {
            'q': keywords,
            'l': location,
            'start': p * 10
        }
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(base_url, params=params, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for card in soup.find_all('div', class_='job_seen_beacon'):
            title_tag = card.find('h2', class_='title') or card.find('a', {'data-jk': True})
            if not title_tag:
                continue
            title = title_tag.get_text(strip=True)
            link = "https://www.indeed.com" + title_tag.find('a')['href'] if title_tag.name == 'h2' else title_tag['href']
            company = card.find('span', {'data-testid': 'company-name'})
            company = company.get_text(strip=True) if company else "Unknown"
            
            # Fetch full description
            time.sleep(random.uniform(1, 3))  # Polite delay
            job_desc = fetch_job_description(link)
            
            jobs.append({
                "title": title,
                "company": company,
                "link": link,
                "description": job_desc
            })
    return jobs
