# utils/postprocessing.py

import os
import sqlite3
import uuid
from PIL import Image

def extract_and_store_objects(image_dir, output_dir, db_path='data/database.db'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Initialize the database
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS objects (id TEXT PRIMARY KEY, master_id TEXT, object_image_path TEXT)''')

    master_id = str(uuid.uuid4())

    for i, filename in enumerate(os.listdir(image_dir)):
        object_id = str(uuid.uuid4())
        object_path = os.path.join(output_dir, f"{object_id}.png")

        # Save object image
        object_image = Image.open(os.path.join(image_dir, filename))
        object_image.save(object_path)

        # Store metadata in the database
        c.execute("INSERT INTO objects VALUES (?, ?, ?)", (object_id, master_id, object_path))

    conn.commit()
    conn.close()

    print(f"Extracted and stored {i+1} objects with master ID {master_id}")

if __name__ == "__main__":
    # Example usage
    segmented_dir = "data/segmented_objects"
    output_directory = "data/segmented_objects/stored_objects"
    
    extract_and_store_objects(segmented_dir, output_directory)
