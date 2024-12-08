# This module defines the `JSONToTXTConverter` class for converting annotation data from JSON format 
# into YOLO-compatible TXT files
# The class includes functionalities for:
# - Extracting unique labels and mapping them to respective files
# - Validating and processing JSON files
# - Calculating YOLO-format bounding boxes from polygon annotations
# - Generating TXT output files in YOLO format
# - Logging every step for debugging and transparency

# The conversion assumes:
# - JSON files contain "shapes" with polygon data
# - Only user-selected labels are processed and included in the output
# - Bounding box calculations are scaled to image dimensions (width and height)
import os
import json
import logging

class JSONToTXTConverter:
    # Handles JSON to YOLO txt

    def __init__(self, input_files, selected_labels):
        self.input_files = input_files if isinstance(input_files, list) else [input_files]
        self.selected_labels = selected_labels
        logging.info(f"Initialized converter with files: {self.input_files} and selected labels: {self.selected_labels}")

    def extract_labels(self):
        # Extract unique labels and map to respective files
        logging.info("Starting label extraction...")
        unique_labels = set()
        file_label_map = {}

        for file_path in self.input_files:
            try:
                logging.debug(f"Reading file: {file_path}")
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    file_labels = {shape['label'] for shape in data.get('shapes', [])}
                    unique_labels.update(file_labels)
                    file_label_map[file_path] = sorted(file_labels)
                    logging.info(f"Extracted labels from {file_path}: {file_labels}")
            except Exception as e:
                logging.error(f"Error reading file {file_path}: {e}")
        
        logging.info(f"Unique labels extracted: {sorted(unique_labels)}")
        return sorted(unique_labels), file_label_map

    def convert_files(self):
        # Convert provided JSON files to YOLO TXT format
        logging.info("Starting file conversion...")
        results = {}

        for file_path in self.input_files:
            try:
                if file_path.endswith('.json') and os.path.isfile(file_path):
                    logging.info(f"Processing file: {file_path}")
                    results[file_path] = self._process_file(file_path)
                else:
                    logging.warning(f"Skipping invalid file: {file_path}")
            except Exception as e:
                logging.error(f"Error converting file {file_path}: {e}")
                results[file_path] = f"Error: {e}"

        logging.info("File conversion completed.")
        return results

    def _process_file(self, file_path):
        # Convert a single JSON file to YOLO txt
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)

            output_file = file_path.replace('.json', '.txt')
            with open(output_file, 'w') as out_file:
                has_data = False
                for shape in data.get('shapes', []):
                    if shape['shape_type'] == "polygon" and shape['label'] in self.selected_labels:
                        has_data = self._write_polygon_data(shape, data, out_file) or has_data

                if not has_data:
                    out_file.write("# No valid polygons found in this file.\n")
                    logging.warning(f"No valid polygons found in file: {file_path}")

            logging.info(f"Successfully converted {file_path} to {output_file}")
            return f"Converted to {output_file}"
        except Exception as e:
            logging.error(f"Error processing file {file_path}: {e}")
            raise

    def _write_polygon_data(self, shape, data, out_file):
        # Write YOLO format polygon data to output
        try:
            points = shape['points']
            x_coords = [p[0] for p in points]
            y_coords = [p[1] for p in points]
            x_min, x_max = min(x_coords), max(x_coords)
            y_min, y_max = min(y_coords), max(y_coords)

            dw = 1.0 / data['imageWidth']
            dh = 1.0 / data['imageHeight']
            x_center = (x_min + x_max) / 2.0 * dw
            y_center = (y_min + y_max) / 2.0 * dh
            w = (x_max - x_min) * dw
            h = (y_max - y_min) * dh

            class_label = self.selected_labels.index(shape['label'])
            out_file.write(f"{class_label} {x_center} {y_center} {w} {h}\n")
            logging.debug(f"Written polygon data for label {shape['label']}: {class_label} {x_center} {y_center} {w} {h}")
            return True
        except ValueError as e:
            logging.warning(f"Label {shape['label']} not found in selected labels: {e}")
            return False
        except Exception as e:
            logging.error(f"Error writing polygon data: {e}")
            raise
