# image_segmentation.py

import torch
from torchvision import models, transforms
from PIL import Image
import matplotlib.pyplot as plt
import cv2
import numpy as np

# Install required packages
# !pip install torch torchvision pillow matplotlib opencv-python

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

def plot_segmented_objects(image_path, prediction, threshold=0.5):
    image = cv2.imread(image_path)
    for i in range(len(prediction[0]['masks'])):
        # Use a threshold to filter weak predictions
        if prediction[0]['scores'][i] > threshold:
            mask = prediction[0]['masks'][i, 0].numpy()
            mask = mask > threshold
            # Create a colored mask
            colored_mask = np.zeros_like(image, dtype=np.uint8)
            colored_mask[mask] = [0, 255, 0]  # Green color for the mask
            image = cv2.addWeighted(image, 1, colored_mask, 0.5, 0)

    plt.figure(figsize=(10, 10))
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    image_path = "input_image.jpg"  # Replace with your image path
    model = load_model()
    image_tensor = preprocess_image(image_path)
    prediction = get_segmented_objects(model, image_tensor)
    plot_segmented_objects(image_path, prediction)
