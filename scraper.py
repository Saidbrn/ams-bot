import requests

def search_jobs(keyword="", location="", max_results=10):
    try:
        url = "https://jobs.ams.at/public/emps/jobs"
        params = {"query": keyword, "location": location}
        
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            "Accept": "application/json",
            "X-Requested-With": "XMLHttpRequest",
        }
        
        r = requests.get(url, params=params, headers=headers, timeout=15)
        print(f"Status: {r.status_code}")
        print(f"Response: {r.text[:500]}")
        
        try:
            data = r.json()
            if isinstance(data, list):
                return data[:max_results]
            elif isinstance(data, dict):
                for key in ["content", "jobs", "data", "results", "items"]:
                    if key in data:
                        return data[key][:max_results]
        except:
            pass
        
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []

def format_job(job):
    title   = job.get("beruf") or job.get("title") or job.get("bezeichnung") or str(job)[:100]
    company = job.get("firma") or job.get("company") or "—"
    loc     = job.get("arbeitsort") or job.get("location") or job.get("ort") or "—"
    email   = job.get("email") or job.get("bewerbungEmail") or "—"
    url     = job.get("url") or job.get("link") or job.get("detailUrl") or ""
    
    return (
        f"💼 *{title}*\n"
        f"🏢 {company}\n"
        f"📍 {loc}\n"
        f"📧 {email}\n"
        f"🔗 {url or 'N/A'}"
    )
