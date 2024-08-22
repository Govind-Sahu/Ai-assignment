# models/summarization_model.py

import openai
import sqlite3

def summarize_object_attributes(db_path='data/database.db'):
    # Initialize the database connection
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("SELECT id, description, extracted_text FROM objects")
    objects = c.fetchall()

    for object_id, description, extracted_text in objects:
        summary = f"Description: {description}, Extracted Text: {extracted_text}"

        # Store the summary back into the database
        c.execute("UPDATE objects SET summary = ? WHERE id = ?", (summary, object_id))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Example usage
    summarize_object_attributes()
    print("Summaries generated for all objects and saved.")
