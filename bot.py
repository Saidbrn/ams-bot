import os
import logging
from telegram.ext import Updater, CommandHandler
from scraper import search_jobs, format_job

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = os.environ.get("BOT_TOKEN")

def start(update, context):
    update.message.reply_text(
        "مرحباً! أنا بوت وظائف AMS\n\n"
        "/jobs — آخر الوظائف\n"
        "/search كلمة — بحث\n"
        "/city مدينة — بحث حسب المدينة"
    )

def latest_jobs(update, context):
    update.message.reply_text("جاري البحث...")
    jobs = search_jobs(max_results=5)
    if not jobs:
        update.message.reply_text("ماكاين والو دابا")
        return
    for job in jobs:
        update.message.reply_text(format_job(job), parse_mode="Markdown")

def search(update, context):
    if not context.args:
        update.message.reply_text("مثال: /search Elektriker")
        return
    keyword = " ".join(context.args)
    update.message.reply_text(f"كنبحث على: {keyword}...")
    jobs = search_jobs(keyword=keyword, max_results=8)
    if not jobs:
        update.message.reply_text(f"ماكاين والو لـ {keyword}")
        return
    for job in jobs:
        update.message.reply_text(format_job(job), parse_mode="Markdown")

def by_city(update, context):
    if not context.args:
        update.message.reply_text("مثال: /city Wien")
        return
    city = " ".join(context.args)
    update.message.reply_text(f"كنبحث في: {city}...")
    jobs = search_jobs(location=city, max_results=8)
    if not jobs:
        update.message.reply_text(f"ماكاين والو في {city}")
        return
    for job in jobs:
        update.message.reply_text(format_job(job), parse_mode="Markdown")

def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("jobs", latest_jobs))
    dp.add_handler(CommandHandler("search", search))
    dp.add_handler(CommandHandler("city", by_city))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
