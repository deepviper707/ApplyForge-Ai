from groq import Groq
import yaml, os

with open("../config/settings.yaml") as f:
    config = yaml.safe_load(f)

client = Groq(api_key=config['llm']['groq_api_key'])

def tailor_resume(base_text, job_desc):
    prompt = f"Tailor resume naturally:\nJob: {job_desc}\nResume: {base_text}"
    resp = client.chat.completions.create(model=config['llm']['model'], messages=[{"role": "user", "content": prompt}])
    return resp.choices[0].message.content

def tailor_cover_letter(template, title, company, job_desc):
    prompt = f"Customize cover letter:\nTemplate: {template}\nTitle: {title}\nCompany: {company}\nJob: {job_desc}"
    resp = client.chat.completions.create(model=config['llm']['model'], messages=[{"role": "user", "content": prompt}])
    return resp.choices[0].message.content
