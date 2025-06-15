from PyPDF2 import PdfReader, PdfWriter
from ebooklib import epub
from PIL import Image
import os

def add_thumbnail_to_pdf(pdf_path, image_path, output_path):
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    with open(image_path, "rb") as f:
        writer.add_attachment("thumbnail.jpg", f.read())

    writer.add_metadata({"/Producer": "Oldtown Bot"})
    with open(output_path, "wb") as f:
        writer.write(f)

def add_thumbnail_to_epub(epub_path, image_path, output_path):
    book = epub.read_epub(epub_path)
    with open(image_path, "rb") as f:
        image_data = f.read()

    img_item = epub.EpubItem(
        uid="cover", file_name="images/cover.jpg",
        media_type="image/jpeg", content=image_data
    )

    book.items.append(img_item)
    book.set_cover("cover.jpg", image_data)
    book.set_title("Oldtown")

    epub.write_epub(output_path, book)
