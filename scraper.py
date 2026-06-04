import requests

def search_jobs(keyword="", location="", max_results=10):
    try:
        # API رسمي ديال Bundesagentur für Arbeit - كيشمل النمسا كذلك
        url = "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v4/jobs"
        headers = {
            "X-API-Key": "jobboerse-jobsuche",
            "User-Agent": "Mozilla/5.0",
        }
        params = {
            "was": keyword,
            "wo": location or "Österreich",
            "page": 1,
            "size": max_results,
        }
        r = requests.get(url, headers=headers, params=params, timeout=15)
        print(f"Status: {r.status_code}")
        data = r.json()
        jobs = data.get("stellenangebote", [])
        return jobs[:max_results]
    except Exception as e:
        print(f"Error: {e}")
        return []

def format_job(job):
    title   = job.get("titel") or "—"
    company = job.get("arbeitgeber") or "—"
    loc     = job.get("arbeitsort", {}).get("ort") or "—"
    date    = job.get("eintrittsdatum") or ""
    ref     = job.get("refnr") or ""
    url     = f"https://www.arbeitsagentur.de/jobsuche/jobdetail/{ref}" if ref else "—"

    return (
        f"💼 *{title}*\n"
        f"🏢 {company}\n"
        f"📍 {loc}\n"
        f"📅 {date}\n"
        f"🔗 {url}"
    )
