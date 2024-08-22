# tests/test_identification.py

import unittest
import sqlite3
from models.identification_model import identify_objects

class TestIdentification(unittest.TestCase):

    def setUp(self):
        self.db_path = "data/database.db"

    def test_identify_objects(self):
        identify_objects(self.db_path)

        # Check if descriptions were added to the database
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT description FROM objects WHERE description IS NOT NULL")
        results = c.fetchall()
        conn.close()

        self.assertGreater(len(results), 0, "Object descriptions should be present in the database.")

    def tearDown(self):
        # Optionally, reset the database for next test runs
        pass

if __name__ == "__main__":
    unittest.main()
