# tests/test_text_extraction.py

import unittest
import sqlite3
from models.text_extraction_model import extract_text_from_objects

class TestTextExtraction(unittest.TestCase):

    def setUp(self):
        self.db_path = "data/database.db"

    def test_extract_text(self):
        extract_text_from_objects(self.db_path)

        # Check if text was extracted and stored in the database
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT extracted_text FROM objects WHERE extracted_text IS NOT NULL")
        results = c.fetchall()
        conn.close()

        self.assertGreater(len(results), 0, "Extracted text should be present in the database.")

    def tearDown(self):
        # Optionally, reset the database for next test runs
        pass

if __name__ == "__main__":
    unittest.main()
