from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from scraper import search_jobs, format_job

BOT_TOKEN = os.environ.get("BOT_TOKEN")

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 مرحباً! أنا بوت وظائف AMS النمسا 🇦🇹\n\n"
        "الأوامر:\n"
        "/jobs — آخر الوظائف\n"
        "/search <كلمة> — بحث بكلمة\n"
        "/city <مدينة> — بحث حسب المدينة\n\n"
        "مثال: /search Mechaniker\n"
        "مثال: /city Graz"
    )

# /jobs — آخر 5 وظائف
async def latest_jobs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ جاري البحث...")
    jobs = search_jobs(max_results=5)
    
    if not jobs:
        await update.message.reply_text("❌ ماكاين والو دابا، عاود من بعد.")
        return
    
    for job in jobs:
        text = format_job(job)
        await update.message.reply_text(text, parse_mode="Markdown")

# /search <keyword>
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("✏️ مثال: /search Elektriker")
        return
    
    keyword = " ".join(context.args)
    await update.message.reply_text(f"🔍 كنبحث على: {keyword}...")
    jobs = search_jobs(keyword=keyword, max_results=8)
    
    if not jobs:
        await update.message.reply_text(f"❌ ماكاين والو لـ '{keyword}'")
        return
    
    await update.message.reply_text(f"✅ لقيت {len(jobs)} وظيفة:")
    for job in jobs:
        text = format_job(job)
        await update.message.reply_text(text, parse_mode="Markdown")

# /city <location>
async def by_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("✏️ مثال: /city Salzburg")
        return
    
    city = " ".join(context.args)
    await update.message.reply_text(f"📍 كنبحث في: {city}...")
    jobs = search_jobs(location=city, max_results=8)
    
    if not jobs:
        await update.message.reply_text(f"❌ ماكاين والو في '{city}'")
        return
    
    await update.message.reply_text(f"✅ لقيت {len(jobs)} وظيفة:")
    for job in jobs:
        text = format_job(job)
        await update.message.reply_text(text, parse_mode="Markdown")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("jobs", latest_jobs))
    app.add_handler(CommandHandler("search", search))
    app.add_handler(CommandHandler("city", by_city))
    app.run_polling()

if __name__ == "__main__":
    main()
