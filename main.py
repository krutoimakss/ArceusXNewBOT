import requests
from bs4 import BeautifulSoup
from telegram.ext import Application, MessageHandler, ContextTypes, filters

BOT_TOKEN = "8778272950:AAFK5lgg3FNx8sOeIHrShblOt2PzX8CSkRk"
CHANNEL = "@ArceusXNew"

DELTA_URL = "https://deltaexploits.gg/delta-executor-android"

LAST_DELTA = None


def get_delta_link():
    r = requests.get(DELTA_URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")

    for a in soup.find_all("a"):
        href = a.get("href")
        if href and (".apk" in href or "download" in href.lower()):
            if href.startswith("/"):
                href = "https://deltaexploits.gg" + href
            return href

    return None


def download_file(url):
    r = requests.get(url, stream=True)
    path = "file.apk"

    with open(path, "wb") as f:
        for chunk in r.iter_content(1024):
            f.write(chunk)

    return path


async def send_delta(app):
    global LAST_DELTA

    url = get_delta_link()
    if not url:
        return

    file_path = download_file(url)

    if file_path == LAST_DELTA:
        return

    LAST_DELTA = file_path

    caption = """tg:ArceusXNew | Delta

🥷 | Delta
⏳ Auto Update

Official: @ArceusXNew"""

    await app.bot.send_document(
        chat_id=CHANNEL,
        document=open(file_path, "rb"),
        caption=caption
    )


async def manual_arceus(update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    if not message.document:
        return

    file = message.document
    filename = file.file_name

    caption = f"""tg:ArceusXNew | ArceusX

🔴 | ArceusX
⏳ Manual Upload: {filename}

Official: @ArceusXNew"""

    await context.bot.send_document(
        chat_id=CHANNEL,
        document=file.file_id,
        caption=caption
    )


app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(MessageHandler(filters.Document.ALL, manual_arceus))


async def loop(app):
    import asyncio
    while True:
        try:
            await send_delta(app)
        except:
            pass
        await asyncio.sleep(300)


app.post_init = lambda app: app.create_task(loop(app))

app.run_polling()
