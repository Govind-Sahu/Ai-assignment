# utils/visualization.py

import json
import cv2
import pandas as pd
import matplotlib.pyplot as plt

def generate_output_image(image_path, annotations, output_path):
    # Load the image
    image = cv2.imread(image_path)

    # Annotate the image with bounding boxes and labels
    for annotation in annotations:
        x, y, w, h = annotation['bbox']
        label = annotation['description']
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(image, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Save the annotated image
    cv2.imwrite(output_path, image)
    print(f"Annotated image saved to {output_path}")

def generate_summary_table(mapping_data, output_csv):
    # Convert the mapping data into a DataFrame
    summary_data = []
    for master_id, data in mapping_data.items():
        for obj in data['objects']:
            row = {
                "Master ID": master_id,
                "Object ID": obj["object_id"],
                "Description": obj["description"],
                "Extracted Text": obj["extracted_text"],
                "Summary": obj["summary"]
            }
            summary_data.append(row)
    
    df = pd.DataFrame(summary_data)
    df.to_csv(output_csv, index=False)
    print(f"Summary table saved to {output_csv}")

if __name__ == "__main__":
    # Example usage
    with open('data/mapped_data.json') as f:
        mapping_data = json.load(f)

    generate_output_image("data/input_images/sample_image.jpg", mapping_data["master_id"]["objects"], "data/output/annotated_image.png")
    generate_summary_table(mapping_data, "data/output/summary_table.csv")
