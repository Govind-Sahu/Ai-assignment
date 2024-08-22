# models/text_extraction_model.py

import pytesseract
from PIL import Image
import sqlite3

def extract_text_from_objects(db_path='data/database.db'):
    # Initialize the database connection
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("SELECT id, object_image_path FROM objects")
    objects = c.fetchall()

    for object_id, image_path in objects:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)

        # Store the extracted text back into the database
        c.execute("UPDATE objects SET extracted_text = ? WHERE id = ?", (text, object_id))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Example usage
    extract_text_from_objects()
    print("Text extracted from all objects and saved.")
