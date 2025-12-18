import requests
from bs4 import BeautifulSoup

def search_indeed(keywords, location="United States", pages=2):
    jobs = []
    for p in range(pages):
        url = f"https://www.indeed.com/jobs?q={keywords}&l={location}&start={p*10}"
        headers = {"User-Agent": "Mozilla/5.0"}
        soup = BeautifulSoup(requests.get(url, headers=headers).text, 'html.parser')
        for card in soup.find_all('div', class_='job_seen_beacon'):
            title = card.find('h2').get_text(strip=True) if card.find('h2') else ""
            company = card.find('span', {'data-testid': 'company-name'}).get_text(strip=True) if card.find('span', {'data-testid': 'company-name'}) else ""
            link = "https://www.indeed.com" + card.find('a')['href']
            jobs.append({"title": title, "company": company, "link": link})
    return jobs
