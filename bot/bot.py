import os, logging, requests, asyncio, json, time, subprocess
from yt_dlp import YoutubeDL
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    MessageHandler, CallbackQueryHandler,
    ContextTypes, filters
)
from telegram.error import TimedOut, NetworkError, BadRequest
##from config import settings
logging.basicConfig(level=logging.INFO)
with open("botLog.txt", "w") as lg:
    lg.write(f'{logging.getLogger(__name__)}\n')

#from api.celery_app import celery
from celery.result import AsyncResult
from pathlib import Path
from config import settings

BOT_TOKEN = setiings.BOT_TOKEN
API_URL = setiings.API_URL
user_data_store = {}
deststr = "downloads"

#______________musicname_________
async def music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎧 *Play Land*\n\n"
        "Enter the song title!\n",
        parse_mode="Markdown",
    )

# ---------------- SEARCH ---------------- #
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE, max_results=10):
    query = update.message.text
    msg_id = update.message.message_id
    print(msg_id)

    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'skip_download': True,
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch{20}:{query}", download=False)
    results = info['entries']
    keyboard = []
    for i, video in enumerate(results):
        title = video['title'][:40]
        keyboard.append([
            InlineKeyboardButton(title, callback_data=f"select_{i}"),
            
            
        ])
    keyboard.append([
        InlineKeyboardButton("Download All", callback_data="download_all"),    
    ])

    user_data_store[update.message.chat_id] = results

    await update.message.reply_text(
        "🔎 Select a result:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    

# ---------------- SELECT VIDEO ---------------- #
async def select_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    urlList = []
    if query.data != "download_all":
        index = int(query.data.split("_")[1])
        video = user_data_store[query.message.chat_id][index]
        url = f"https://youtube.com/watch?v={video['id']}"
        context.user_data['url'] = url
        
        keyboard = [
        [
            InlineKeyboardButton("🎵 Audio (MP3)", callback_data="audio"),
            InlineKeyboardButton("🎬 Video (MP4)", callback_data="video")
        ]]

        await query.edit_message_text(
            f"🎬 *{video['title']}*\n\nChoose format:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    else:
        videoList = user_data_store[query.message.chat_id]
        for i in videoList:
            url = f"https://youtube.com/watch?v={i['id']}"
            urlList.append(url)
        
        context.user_data['url'] = urlList
        keyboard = [
        [
            InlineKeyboardButton("🎵 Audio (MP3)", callback_data="audio"),
            InlineKeyboardButton("🎬 Video (MP4)", callback_data="video")
        ]]
        
        await query.edit_message_text(
            f"🎬 *Download All*\n\nChoose format:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        

    


# ---------------- FORMAT ---------------- #
async def choose_format(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    choice = query.data
    context.user_data['format'] = choice

    if choice == "audio":
        keyboard = [
            [InlineKeyboardButton("128 kbps", callback_data="128")],
            [InlineKeyboardButton("192 kbps", callback_data="192")],
            [InlineKeyboardButton("320 kbps", callback_data="320")]
        ]
    else:
        keyboard = [
            [InlineKeyboardButton("360p", callback_data="360")],
            [InlineKeyboardButton("720p", callback_data="720")],
            [InlineKeyboardButton("1080p", callback_data="1080")]
        ]

    await query.edit_message_text(
        "⚙ Select quality:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ---------------- DOWNLOAD ---------------- #
async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    quality = query.data
    url = context.user_data['url']
    format_type = context.user_data['format']
    res = requests.post(f'{API_URL}/downloads', json={
        'url': url,
        'quality': quality,
        'format_type': format_type,
    })
    
    msg = await query.edit_message_text("⏳ Downloading...")
    
    task_id = res.json()["task_id"]
    #resultss = AsyncResult(task_id)
    max_retries = 10
    attempts = 0
    while True:
        await asyncio.sleep(2)
        task = requests.get(f'{API_URL}/status/{task_id}').json()
        if task["status"] == "SUCCESS":
            filenameInfo = task["result"]
            
            await msg.edit_text("✅ Done")
            time.sleep(2)
            break
        elif task["status"] == "FAILURE":
            await msg.edit_text("Failed.....")
            break
        else:
            pass
    
    filename = filenameInfo["filename"]
    lisfiles = subprocess.check_output(f'ls downloads', shell=True, text=True)
    catlis = [fle for fle in lisfiles.splitlines() if fle]
    if len(catlis) != 0:
        try:
            os.chdir("./downloads")        
            for i in catlis:
                os.rename(i, filename)
            os.chdir("../")
        except Exception as e:
            boterror = {
                "Error": str(e)    
            }
            with open("boterror.json", "w") as bote:
                json(boterror, bote, indent=2)
    else:
        pass
        
    filePath = Path(deststr)
    file_path = f"{deststr}/{filename}"
    await msg.edit_text(f"🌟  {filename}  🌟")
    for i in range(max_retries):
        try:            
            await query.message.reply_document(open(file_path, 'rb'))
            break
        except TimedOut:
            if attempts < max_retries -1:
                time.sleep(5)
            else:
                await msg.edit_text("Connection Failed.....")
                print("Check Connection")
                continue
    os.remove(file_path)
        



# ---------------- START ---------------- #
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎧 *Play Land*\n\n\n"
        "🌟 Welcome to your One Stop Downloader 🌟\n\n"
        "      🎧 Music\n"
        "      🎬 Movie Trailers\n"
        "      🛜 Movie Torrents\n\n\n"
        "✨ Usage ✨\n\n"
        "      ✅ Send any name to search\n",
        parse_mode="Markdown",
    )

if __name__ == "__main__":
    # ---------------- MAIN ---------------- #
    max_retries = 10
    attempts = 0
    for i in range(max_retries):
        try:
            app = ApplicationBuilder().token(BOT_TOKEN).build()
            ##app start
            app.add_handler(CommandHandler("start", start))
            ##music
            app.add_handler(CommandHandler("music", music))
            app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))
            app.add_handler(CallbackQueryHandler(select_video, pattern="^select_"))
            app.add_handler(CallbackQueryHandler(choose_format, pattern="^(audio|video)$"))
            app.add_handler(CallbackQueryHandler(download, pattern="^(128|192|320|360|720|1080)$"))
    
            app.run_polling(poll_interval=1, timeout=600)
        
        except TimedOut:
            if attempts < max_retries -1:
                time.sleep(5)
            else:
                print("Error: NetworkError")
                continue

