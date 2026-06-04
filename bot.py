import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from scraper import search_jobs, format_job

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "مرحباً! أنا بوت وظائف AMS\n\n"
        "/jobs — آخر الوظائف\n"
        "/search كلمة\n"
        "/city مدينة"
    )

async def latest_jobs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("جاري البحث...")
    jobs = search_jobs(max_results=5)
    if not jobs:
        await update.message.reply_text("ماكاين والو دابا")
        return
    for job in jobs:
        await update.message.reply_text(format_job(job), parse_mode="Markdown")

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("مثال: /search Elektriker")
        return
    keyword = " ".join(context.args)
    jobs = search_jobs(keyword=keyword, max_results=8)
    if not jobs:
        await update.message.reply_text(f"ماكاين والو لـ {keyword}")
        return
    for job in jobs:
        await update.message.reply_text(format_job(job), parse_mode="Markdown")

async def by_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("مثال: /city Wien")
        return
    city = " ".join(context.args)
    jobs = search_jobs(location=city, max_results=8)
    if not jobs:
        await update.message.reply_text(f"ماكاين والو في {city}")
        return
    for job in jobs:
        await update.message.reply_text(format_job(job), parse_mode="Markdown")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("jobs", latest_jobs))
    app.add_handler(CommandHandler("search", search))
    app.add_handler(CommandHandler("city", by_city))
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
