# object_extraction.py

import cv2
import numpy as np
import os
import sqlite3
from PIL import Image
import torch
from torchvision import models, transforms

# Install required packages
# !pip install torch torchvision pillow opencv-python sqlite3

def create_database():
    conn = sqlite3.connect('object_metadata.db')
    cursor = conn.cursor()
    
    # Create table to store metadata
    cursor.execute('''CREATE TABLE IF NOT EXISTS objects (
                        id INTEGER PRIMARY KEY,
                        master_id TEXT,
                        object_id TEXT,
                        file_path TEXT
                      )''')
    conn.commit()
    conn.close()

def save_metadata(master_id, object_id, file_path):
    conn = sqlite3.connect('object_metadata.db')
    cursor = conn.cursor()
    
    cursor.execute('''INSERT INTO objects (master_id, object_id, file_path)
                      VALUES (?, ?, ?)''', (master_id, object_id, file_path))
    
    conn.commit()
    conn.close()

def extract_and_save_objects(image_path, prediction, output_dir="output"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    master_id = os.path.basename(image_path).split('.')[0]  # Use image name as master_id
    
    for i, mask in enumerate(prediction[0]['masks']):
        # Use a threshold to filter weak predictions
        mask = mask[0].numpy() > 0.5
        
        # Extract the object using the mask
        image = cv2.imread(image_path)
        object_image = cv2.bitwise_and(image, image, mask=mask.astype(np.uint8))
        
        # Generate a unique ID for the object
        object_id = f"{master_id}_obj_{i+1}"
        
        # Save the object image
        object_image_path = os.path.join(output_dir, f"{object_id}.png")
        cv2.imwrite(object_image_path, object_image)
        
        # Save the metadata in the database
        save_metadata(master_id, object_id, object_image_path)

def load_model():
    # Load a pre-trained Mask R-CNN model
    model = models.detection.maskrcnn_resnet50_fpn(pretrained=True)
    model.eval()
    return model

def preprocess_image(image_path):
    # Define the standard transformation
    transform = transforms.Compose([
        transforms.ToTensor()
    ])
    image = Image.open(image_path).convert("RGB")
    image_tensor = transform(image)
    return image_tensor

def get_segmented_objects(model, image_tensor):
    # Add a batch dimension and pass the image through the model
    with torch.no_grad():
        prediction = model([image_tensor])

    return prediction

if __name__ == "__main__":
    image_path = "input_image.jpg"  # Replace with your image path
    output_dir = "output_objects"
    
    # Step 1: Create database for metadata storage
    create_database()

    # Step 2: Load the model and preprocess the image
    model = load_model()
    image_tensor = preprocess_image(image_path)
    
    # Step 3: Get segmented objects from the image
    prediction = get_segmented_objects(model, image_tensor)
    
    # Step 4: Extract and save objects
    extract_and_save_objects(image_path, prediction, output_dir)
