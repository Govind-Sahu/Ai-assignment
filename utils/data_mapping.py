# utils/data_mapping.py

import sqlite3
import json

def map_data_to_json(db_path='data/database.db', json_file='data/mapped_data.json'):
    # Initialize the database connection
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Fetch all data from the database
    c.execute("SELECT id, master_id, object_image_path, description, extracted_text, summary FROM objects")
    objects = c.fetchall()

    # Structure the data
    mapping_data = {}
    for object_id, master_id, image_path, description, text, summary in objects:
        if master_id not in mapping_data:
            mapping_data[master_id] = {"objects": []}

        mapping_data[master_id]["objects"].append({
            "object_id": object_id,
            "image_path": image_path,
            "description": description,
            "extracted_text": text,
            "summary": summary
        })

    # Save the mapping data to a JSON file
    with open(json_file, 'w') as file:
        json.dump(mapping_data, file, indent=4)

    conn.close()
    print(f"Data mapping saved to {json_file}")

if __name__ == "__main__":
    # Example usage
    map_data_to_json()
