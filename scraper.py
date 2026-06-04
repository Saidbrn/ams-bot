import requests
from datetime import datetime, timedelta

def search_jobs(keyword="", location="", max_results=10):
    try:
        url = "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v4/jobs"
        headers = {
            "X-API-Key": "jobboerse-jobsuche",
            "User-Agent": "Mozilla/5.0",
        }
        params = {
            "was": keyword,
            "wo": location or "Österreich",
            "page": 1,
            "size": 50,  # نجيبو كثر باش نفيلترو
        }
        r = requests.get(url, headers=headers, params=params, timeout=15)
        data = r.json()
        jobs = data.get("stellenangebote", [])

        # فيلتر آخر 5 أيام
        cutoff = datetime.now() - timedelta(days=5)
        filtered = []
        for job in jobs:
            date_str = job.get("aktuelleVeroeffentlichungsdatum") or job.get("eintrittsdatum") or ""
            try:
                job_date = datetime.strptime(date_str[:10], "%Y-%m-%d")
                if job_date >= cutoff:
                    filtered.append(job)
            except:
                filtered.append(job)  # إلا ماعندوش تاريخ نضيفو على كل حال
            if len(filtered) >= max_results:
                break

        return filtered
    except Exception as e:
        print(f"Error: {e}")
        return []

def get_job_email(refnr):
    """جيب إيميل الشركة من صفحة التفاصيل"""
    try:
        import base64
        encoded = base64.b64encode(refnr.encode()).decode()
        url = f"https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v4/jobdetails/{encoded}"
        headers = {"X-API-Key": "jobboerse-jobsuche", "User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()
        # دور على الإيميل في التفاصيل
        kontakt = data.get("stellenbeschreibung", "")
        arbeitgeber = data.get("arbeitgeberAdresse", {})
        email = arbeitgeber.get("email") or ""
        return email
    except:
        return ""

def format_job(job):
    title   = job.get("titel") or "—"
    company = job.get("arbeitgeber") or "—"
    loc     = job.get("arbeitsort", {}).get("ort") or "—"
    date    = job.get("aktuelleVeroeffentlichungsdatum") or job.get("eintrittsdatum") or ""
    ref     = job.get("refnr") or ""
    url     = f"https://www.arbeitsagentur.de/jobsuche/jobdetail/{ref}" if ref else "—"
    
    # جيب الإيميل
    email = get_job_email(ref) if ref else ""
    email_line = f"📧 {email}\n" if email else "📧 —\n"

    return (
        f"💼 *{title}*\n"
        f"🏢 {company}\n"
        f"📍 {loc}\n"
        f"📅 {date[:10] if date else '—'}\n"
        f"{email_line}"
        f"🔗 {url}"
    )
