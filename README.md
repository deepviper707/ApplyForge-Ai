ApplyForge-AI 🚀
AI-powered job application toolkit. Searches jobs (Indeed & LinkedIn), fetches full descriptions, semantically matches to your resume, tailors resume/cover letter with LLM, automates browser applying (Playwright), tracks everything in SQLite.
Built by Adrian James.
Features

Job searching (Indeed/LinkedIn)
Full job description fetching
Semantic similarity matching (sentence-transformers)
LLM-powered resume & cover letter tailoring (Groq)
Browser automation stub
SQLite database tracking

Requirements
Python 3.9+
Setup (Step-by-Step)

Clone repositoryBashgit clone https://github.com/yourusername/ApplyForge-AI.git
cd ApplyForge-AI
Install dependenciesBashpip install -r requirements.txt
playwright install
Get Groq API key
Go to https://console.groq.com/keys
Create free API key
Edit config/settings.yaml → add key to groq_api_key: "your_key_here"

Prepare your documents
Place your base resume as plain text: data/base_resume.txt (copy content from DOCX/PDF)
Optional: Add data/base_cover_letter.txt (universal template)

Configure search
Edit config/settings.yaml:
keywords: your target roles
site: "indeed" or "linkedin"
min_similarity_threshold: 0.65 recommended


Initialize database
First run creates data/applyforge.db automatically


Usage
Run the main script:
Bashpython src/main.py
What happens:

Searches selected site
Fetches full job descriptions (concurrent for speed)
Computes semantic match score with your resume
Saves strong matches to database
(Future: auto-tailor & apply)

View tracked jobs: Open data/applyforge.db with any SQLite viewer (DB Browser for SQLite).
Warnings

Scraping may violate site ToS — personal use only, low volume
Add delays/proxies if blocked
Never auto-apply blindly

Next Steps (Expand Yourself)

Integrate tailoring (call tailor.py)
Add Playwright Easy Apply logic
Export tailored docs to outputs/

MIT License. Star if useful!
