import requests
import xml.etree.ElementTree as ET

def search_jobs(keyword="", location="", max_results=10):
    # RSS Feed رسمي ديال AMS
    url = "https://www.ams.at/rss/stellen.xml"
    try:
        r = requests.get(url, timeout=15, headers={
            "User-Agent": "Mozilla/5.0"
        })
        root = ET.fromstring(r.content)
        items = root.findall(".//item")
        jobs = []
        for item in items:
            title = item.findtext("title") or "—"
            link  = item.findtext("link") or ""
            desc  = item.findtext("description") or ""
            
            # فيلتر بكلمة البحث
            if keyword and keyword.lower() not in title.lower() and keyword.lower() not in desc.lower():
                continue
            if location and location.lower() not in desc.lower():
                continue
            
            jobs.append({
                "title": title,
                "description": desc[:200],
                "url": link,
            })
            if len(jobs) >= max_results:
                break
        return jobs
    except Exception as e:
        print(f"Error: {e}")
        return []

def format_job(job):
    return (
        f"💼 *{job.get('title','—')}*\n"
        f"📝 {job.get('description','—')}\n"
        f"🔗 {job.get('url','N/A')}"
    )
