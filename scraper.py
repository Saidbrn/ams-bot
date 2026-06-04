import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
    "Referer": "https://jobs.ams.at/",
}

def search_jobs(keyword="", location="Wien", max_results=10):
    url = "https://jobs.ams.at/public/emps/api/jobs"
    params = {
        "q": keyword,
        "ort": location,
        "page": 0,
        "size": max_results,
    }
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=10)
        r.raise_for_status()
        data = r.json()
        jobs = data.get("content", []) or data.get("jobs", []) or data
        return jobs
    except Exception as e:
        return []

def format_job(job):
    title     = job.get("beruf") or job.get("title") or "—"
    company   = job.get("firma") or job.get("company") or "—"
    location  = job.get("arbeitsort") or job.get("ort") or "—"
    email     = job.get("email") or job.get("bewerbungEmail") or "—"
    url       = job.get("url") or job.get("link") or ""
    job_id    = job.get("id") or ""
    
    if not url and job_id:
        url = f"https://jobs.ams.at/public/emps/jobs/{job_id}"
    
    return (
        f"💼 *{title}*\n"
        f"🏢 {company}\n"
        f"📍 {location}\n"
        f"📧 {email}\n"
        f"🔗 {url if url else 'N/A'}"
    )