# tests/test_segmentation.py

import unittest
import os
from models.segmentation_model import segment_image

class TestSegmentation(unittest.TestCase):

    def setUp(self):
        self.image_path = "data/input_images/sample_image.jpg"
        self.output_dir = "data/segmented_objects"

    def test_segment_image(self):
        num_objects, boxes = segment_image(self.image_path, self.output_dir)
        
        # Ensure segmentation function returns the correct number of objects
        self.assertGreater(num_objects, 0, "Segmentation should detect at least one object.")
        
        # Ensure output directory contains segmented object images
        self.assertTrue(os.path.exists(self.output_dir), "Segmented objects directory should exist.")
        self.assertGreater(len(os.listdir(self.output_dir)), 0, "Segmented objects should be saved.")

    def tearDown(self):
        # Clean up generated files
        for file in os.listdir(self.output_dir):
            os.remove(os.path.join(self.output_dir, file))

if __name__ == "__main__":
    unittest.main()
