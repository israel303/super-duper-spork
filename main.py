import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile
from aiogram.utils import executor
from dotenv import load_dotenv

from Utils import add_thumbnail_to_pdf, add_thumbnail_to_epub

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

DEFAULT_THUMB = "default_thumb.jpg"

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("👋 שלח קובץ PDF או EPUB כדי לקבל אותו עם thumbnail וכיתוב Oldtown.")

@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def handle_document(message: types.Message):
    document = message.document
    file_name = document.file_name.lower()

    if not (file_name.endswith(".pdf") or file_name.endswith(".epub")):
        await message.reply("⚠️ רק קבצי PDF או EPUB נתמכים.")
        return

    file_path = f"temp/{document.file_name}"
    await document.download(destination_file=file_path)

    output_path = f"temp/output_{document.file_name}"

    try:
        if file_name.endswith(".pdf"):
            add_thumbnail_to_pdf(file_path, DEFAULT_THUMB, output_path)
        else:
            add_thumbnail_to_epub(file_path, DEFAULT_THUMB, output_path)

        await message.reply_document(InputFile(output_path), caption="📄 הנה הקובץ שלך עם כיתוב Oldtown.")
    except Exception as e:
        await message.reply(f"❌ שגיאה: {e}")
    finally:
        if os.path.exists(file_path): os.remove(file_path)
        if os.path.exists(output_path): os.remove(output_path)

if __name__ == '__main__':
    os.makedirs("temp", exist_ok=True)
    executor.start_polling(dp, skip_updates=True)
