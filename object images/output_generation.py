# output_generation.py

import sqlite3
import json
import cv2
import matplotlib.pyplot as plt
import pandas as pd

def load_mapping_data(json_file='mapped_data.json'):
    with open(json_file, 'r') as file:
        data = json.load(file)
    return data

def annotate_image(image_path, annotations, output_path):
    # Load the image
    image = cv2.imread(image_path)

    # Loop over the annotations and draw bounding boxes and labels
    for annotation in annotations:
        x, y, w, h = annotation['bbox']  # Assume bounding box is provided
        object_id = annotation['object_id']
        label = annotation['description']

        # Draw the bounding box
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Draw the label
        cv2.putText(image, f"ID: {object_id} - {label}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Save the annotated image
    cv2.imwrite(output_path, image)
    print(f"Annotated image saved to {output_path}")

def create_summary_table(mapping_data, output_csv='summary_table.csv'):
    # Convert the mapping data into a DataFrame
    summary_data = []

    for master_id, master_data in mapping_data.items():
        for obj in master_data['objects']:
            row = {
                "Master ID": master_id,
                "Object ID": obj["object_id"],
                "Description": obj["description"],
                "Extracted Text": obj["extracted_text"],
                "Summary": obj["summary"]
            }
            summary_data.append(row)
    
    df = pd.DataFrame(summary_data)

    # Save the summary table as a CSV file
    df.to_csv(output_csv, index=False)
    print(f"Summary table saved to {output_csv}")

def plot_summary_table(image_path, summary_table, output_path):
    # Load the image
    image = plt.imread(image_path)

    # Create a figure with image and table side by side
    fig, axs = plt.subplots(1, 2, figsize=(15, 10))

    # Show the image on the left
    axs[0].imshow(image)
    axs[0].axis('off')

    # Display the summary table on the right
    axs[1].axis('off')
    axs[1].table(cellText=summary_table.values, colLabels=summary_table.columns, cellLoc='center', loc='center')

    # Save the final visual output
    plt.savefig(output_path)
    print(f"Final output saved to {output_path}")

if __name__ == "__main__":
    # Load the mapping data from the JSON file
    mapping_data = load_mapping_data()

    # Specify the paths to the original image and the output files
    original_image_path = 'original_image.jpg'
    annotated_image_path = 'annotated_image.jpg'
    summary_table_csv = 'summary_table.csv'
    final_output_path = 'final_output.png'

    # Example annotations with bounding boxes (this would come from earlier steps)
    annotations = [
        {"bbox": (50, 50, 100, 100), "object_id": 101, "description": "A red apple"},
        {"bbox": (200, 50, 100, 100), "object_id": 102, "description": "A bottle of water"}
    ]

    # Step 1: Annotate the original image
    annotate_image(original_image_path, annotations, annotated_image_path)

    # Step 2: Create a summary table
    create_summary_table(mapping_data, summary_table_csv)

    # Step 3: Load the summary table into a DataFrame
    summary_table_df = pd.read_csv(summary_table_csv)

    # Step 4: Plot the final output with the annotated image and the summary table
    plot_summary_table(annotated_image_path, summary_table_df, final_output_path)
