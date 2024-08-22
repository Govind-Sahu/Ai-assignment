# streamlit_app/app.py

import streamlit as st
from PIL import Image
import os
import json
from utils.visualization import generate_output_image, generate_summary_table

def load_json(json_file):
    with open(json_file, 'r') as f:
        return json.load(f)

st.title("Image Segmentation and Analysis Pipeline")

# File uploader
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Save the uploaded file to input_images directory
    image_path = os.path.join("data/input_images", uploaded_file.name)
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.image(image_path, caption='Uploaded Image', use_column_width=True)

    # Process the image
    st.write("Processing...")
    num_objects, boxes = segment_image(image_path, "data/segmented_objects")
    extract_and_store_objects("data/segmented_objects", "data/segmented_objects/stored_objects")
    identify_objects()
    extract_text_from_objects()
    summarize_object_attributes()
    map_data_to_json()

    # Load the mapping data
    mapping_data = load_json("data/mapped_data.json")

    # Generate output
    output_image_path = "data/output/annotated_image.png"
    generate_output_image(image_path, mapping_data['master_id']['objects'], output_image_path)
    summary_table_path = "data/output/summary_table.csv"
    generate_summary_table(mapping_data, summary_table_path)

    st.image(output_image_path, caption='Annotated Image', use_column_width=True)
    st.write("Summary Table:")
    st.write(pd.read_csv(summary_table_path))
