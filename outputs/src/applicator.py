from playwright.sync_api import sync_playwright
import time, random

def apply_with_playwright(job_url, resume_path):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(job_url)
        # Add filling logic here
        time.sleep(random.uniform(8, 15))
        browser.close()
