import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile
from aiogram.utils import executor
from PyPDF2 import PdfReader, PdfWriter
from ebooklib import epub
from PIL import Image

API_TOKEN = os.getenv("BOT_TOKEN")
DEFAULT_THUMB = "default_thumb.jpg"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def handle_document(message: types.Message):
    file = message.document
    file_name = file.file_name.lower()
    if file_name.endswith(".pdf"):
        await handle_pdf(message, file)
    elif file_name.endswith(".epub"):
        await handle_epub(message, file)
    else:
        await message.reply("שלח קובץ PDF או EPUB בלבד.")

async def handle_pdf(message, file):
    file_path = f"temp/{file.file_name}"
    os.makedirs("temp", exist_ok=True)
    await file.download(destination=file_path)

    # פתיחת PDF
    reader = PdfReader(file_path)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)

    # הוספת מטאדאטה עם כותרת
    writer.add_metadata({
        "/Title": "Oldtown PDF"
    })

    new_file_path = f"temp/oldtown_{file.file_name}"
    with open(new_file_path, "wb") as f:
        writer.write(f)

    await message.reply_document(InputFile(new_file_path), caption="📄 הנה הקובץ שלך עם כיתוב Oldtown.")

async def handle_epub(message, file):
    file_path = f"temp/{file.file_name}"
    os.makedirs("temp", exist_ok=True)
    await file.download(destination=file_path)

    book = epub.read_epub(file_path)

    # שינוי התמונה הקבועה
    with open(DEFAULT_THUMB, 'rb') as img_file:
        img_content = img_file.read()

    # הוספת או החלפת התמונה הקיימת
    new_img = epub.EpubItem(uid="cover", file_name="cover.jpg", media_type="image/jpeg", content=img_content)
    book.items.append(new_img)
    book.set_cover("cover.jpg", img_content)

    new_file_path = f"temp/oldtown_{file.file_name}"
    epub.write_epub(new_file_path, book)

    await message.reply_document(InputFile(new_file_path), caption="📄 הנה הקובץ שלך עם כיתוב Oldtown.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
