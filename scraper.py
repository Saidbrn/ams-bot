import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "de-AT,de;q=0.9",
    "Referer": "https://jobs.ams.at/",
    "Origin": "https://jobs.ams.at",
}

def search_jobs(keyword="", location="", max_results=10):
    url = "https://jobs.ams.at/public/emps/api/v1/jobs"
    params = {
        "query": keyword,
        "location": location,
        "page": 0,
        "size": max_results,
    }
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=15)
        data = r.json()
        jobs = []
        if isinstance(data, list):
            jobs = data
        elif isinstance(data, dict):
            jobs = data.get("content") or data.get("jobs") or data.get("data") or []
        return jobs[:max_results]
    except Exception as e:
        print(f"Error: {e}")
        return []

def format_job(job):
    title   = job.get("beruf") or job.get("title") or job.get("bezeichnung") or "—"
    company = job.get("firma") or job.get("company") or job.get("unternehmen") or "—"
    location= job.get("arbeitsort") or job.get("ort") or job.get("location") or "—"
    email   = job.get("email") or job.get("bewerbungEmail") or "—"
    link    = job.get("url") or job.get("link") or job.get("detailUrl") or ""
    job_id  = job.get("id") or ""
    if not link and job_id:
        link = f"https://jobs.ams.at/public/emps/jobs/{job_id}"

    return (
        f"💼 *{title}*\n"
        f"🏢 {company}\n"
        f"📍 {location}\n"
        f"📧 {email}\n"
        f"🔗 {link if link else 'N/A'}"
    )
