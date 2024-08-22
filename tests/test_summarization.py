# tests/test_summarization.py

import unittest
import sqlite3
from models.summarization_model import summarize_object_attributes

class TestSummarization(unittest.TestCase):

    def setUp(self):
        self.db_path = "data/database.db"

    def test_summarize_attributes(self):
        summarize_object_attributes(self.db_path)

        # Check if summaries were generated and stored in the database
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT summary FROM objects WHERE summary IS NOT NULL")
        results = c.fetchall()
        conn.close()

        self.assertGreater(len(results), 0, "Summaries should be present in the database.")

    def tearDown(self):
        # Optionally, reset the database for next test runs
        pass

if __name__ == "__main__":
    unittest.main()
