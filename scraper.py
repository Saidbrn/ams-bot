import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "de-AT,de;q=0.9",
}

def search_jobs(keyword="", location="", max_results=10):
    url = "https://jobs.ams.at/public/emps/jobs"
    params = {}
    if keyword:
        params["query"] = keyword
    if location:
        params["location"] = location
    params["page"] = 0

    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")
        jobs = []
        cards = soup.select(".job-card, .stelle, .result-item, article")[:max_results]
        for card in cards:
            title   = card.select_one("h2, h3, .title, .beruf")
            company = card.select_one(".company, .firma, .unternehmen")
            loc     = card.select_one(".location, .ort, .arbeitsort")
            link    = card.select_one("a")
            jobs.append({
                "title":   title.get_text(strip=True) if title else "—",
                "company": company.get_text(strip=True) if company else "—",
                "location": loc.get_text(strip=True) if loc else "—",
                "url": "https://jobs.ams.at" + link["href"] if link and link.get("href","").startswith("/") else (link["href"] if link else ""),
            })
        return jobs
    except Exception as e:
        print(f"Error: {e}")
        return []

def format_job(job):
    return (
        f"💼 *{job.get('title','—')}*\n"
        f"🏢 {job.get('company','—')}\n"
        f"📍 {job.get('location','—')}\n"
        f"🔗 {job.get('url','N/A')}"
    )
