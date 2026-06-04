import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from scraper import search_jobs, format_job

BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "مرحباً! أنا بوت وظائف AMS\n\n"
        "/jobs — آخر الوظائف\n"
        "/search كلمة — بحث\n"
        "/city مدينة — بحث حسب المدينة"
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
    keyword =
