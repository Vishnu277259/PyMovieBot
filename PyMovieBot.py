from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import requests

# Your TMDB API and Telegram Bot Token
TMDB_API_KEY = '7a31d968ab7ca74252d16d2664dbbe16'
TELEGRAM_BOT_TOKEN = '8189108148:AAE3J8oLG-6x9nIiMwG_bH7N9O-S80JjRCE'

# TMDB API Search
def search_movie_tmdb(query):
    url = f'https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("results", [])[:3]  # Return top 3 results
    return []

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎬 Welcome to Movie Search Engine!\nType a movie name to get details.")

# On user message (movie search)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    movies = search_movie_tmdb(query)
    if not movies:
        await update.message.reply_text("❌ No movie found.")
        return

    for movie in movies:
        title = movie.get("title")
        overview = movie.get("overview", "No description available.")
        release = movie.get("release_date", "N/A")
        poster_path = movie.get("poster_path")
        link = f"https://www.themoviedb.org/movie/{movie.get('id')}"

        message = f"🎬 *{title}*\n📅 Release Date: {release}\n📝 {overview}\n🔗 [More Info]({link})"
        if poster_path:
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
            await update.message.reply_photo(photo=poster_url, caption=message, parse_mode='Markdown')
        else:
            await update.message.reply_text(message, parse_mode='Markdown')

# Build and run the application
app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Save the code as a file
with open("/mnt/data/movie_bot.py", "w") as f:
    f.write("""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import requests

TMDB_API_KEY = '7a31d968ab7ca74252d16d2664dbbe16'
TELEGRAM_BOT_TOKEN = '8189108148:AAE3J8oLG-6x9nIiMwG_bH7N9O-S80JjRCE'

def search_movie_tmdb(query):
    url = f'https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("results", [])[:3]
    return []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎬 Welcome to Movie Search Engine!\\nType a movie name to get details.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    movies = search_movie_tmdb(query)
    if not movies:
        await update.message.reply_text("❌ No movie found.")
        return

    for movie in movies:
        title = movie.get("title")
        overview = movie.get("overview", "No description available.")
        release = movie.get("release_date", "N/A")
        poster_path = movie.get("poster_path")
        link = f"https://www.themoviedb.org/movie/{movie.get('id')}"

        message = f"🎬 *{title}*\\n📅 Release Date: {release}\\n📝 {overview}\\n🔗 [More Info]({link})"
        if poster_path:
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
            await update.message.reply_photo(photo=poster_url, caption=message, parse_mode='Markdown')
        else:
            await update.message.reply_text(message, parse_mode='Markdown')

app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
""")
