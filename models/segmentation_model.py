# models/segmentation_model.py

import torch
import torchvision
from PIL import Image
import numpy as np
import cv2
import os

def segment_image(image_path, output_dir):
    # Load a pre-trained Mask R-CNN model
    model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)
    model.eval()

    # Load the image
    image = Image.open(image_path).convert("RGB")
    image_tensor = torchvision.transforms.functional.to_tensor(image)

    # Perform inference
    with torch.no_grad():
        prediction = model([image_tensor])[0]

    # Extract masks, bounding boxes, and labels
    masks = prediction['masks'].numpy()
    boxes = prediction['boxes'].numpy()
    labels = prediction['labels'].numpy()

    # Save segmented objects
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i, mask in enumerate(masks):
        segmented_object = (mask[0] * 255).astype(np.uint8)
        segmented_object = cv2.bitwise_and(np.array(image), np.array(image), mask=segmented_object)
        
        cv2.imwrite(f"{output_dir}/object_{i+1}.png", segmented_object)
        cv2.rectangle(np.array(image), (int(boxes[i][0]), int(boxes[i][1])), (int(boxes[i][2]), int(boxes[i][3])), (0, 255, 0), 2)
    
    cv2.imwrite(f"{output_dir}/segmented_image.png", np.array(image))
    return len(masks), boxes

if __name__ == "__main__":
    # Example usage
    input_image_path = "data/input_images/sample_image.jpg"
    output_directory = "data/segmented_objects"
    
    num_objects, boxes = segment_image(input_image_path, output_directory)
    print(f"Segmented {num_objects} objects.")
