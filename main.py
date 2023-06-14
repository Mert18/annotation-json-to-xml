import os
import json
import xml.etree.ElementTree as ET

# Define the input and output directories
json_dir = './images'
xml_dir = './xmls'

# Create the output directory if it doesn't exist
os.makedirs(xml_dir, exist_ok=True)

# Function to convert extracted data to XML
def get_min_max_points(json_data):
    # Get the "points" field from the JSON data
    points = json_data.get('points', [])

    if not points:
        return None

    min_x = float('inf')
    max_x = float('-inf')
    min_y = float('inf')
    max_y = float('-inf')

    # Iterate over the points and update the minimum and maximum values
    for point in points:
        if len(point) >= 2:
            x, y = point[:2]
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)

    return {
        'min_x': int(min_x),
        'max_x': int(max_x),
        'min_y': int(min_y),
        'max_y': int(max_y)
    }

# Iterate over the JSON files in the input directory
for filename in os.listdir(json_dir):
    if filename.endswith('.json'):
        json_path = os.path.join(json_dir, filename)
        xml_filename = os.path.splitext(filename)[0] + '.xml'
        xml_path = os.path.join(xml_dir, xml_filename)

        # Read the JSON file
        with open(json_path) as json_file:
            data = json.load(json_file)
            # Extract the desired fields from the JSON
            metadata = {
                  'width': data['image']['width'],
                  'height': data['image']['height'],
                  'image_name': data['image']['image_name']
            }
             # Create the XML structure
            root = ET.Element('annotation')

            

            folder = ET.SubElement(root, 'folder')
            folder.text = 'images'

            file_name= ET.SubElement(root, 'filename')
            file_name.text = metadata['image_name']

            size = ET.SubElement(root, 'size')
            width_element = ET.SubElement(size, 'width')
            width_element.text = str(metadata['width'])
            height_element = ET.SubElement(size, 'height')
            height_element.text = str(metadata['height'])

            for annotation in data['annotations']:
                  object = ET.SubElement(root, 'object')
                  name = ET.SubElement(object, 'name')
                  name.text = annotation['label_name']
                  bndbox = ET.SubElement(object, 'bndbox')

                  bounds = get_min_max_points(annotation)
                  xmin = ET.SubElement(bndbox, 'xmin')
                  xmin.text = str(bounds['min_x'])
                  ymin = ET.SubElement(bndbox, 'ymin')
                  ymin.text = str(bounds['min_y'])
                  xmax = ET.SubElement(bndbox, 'xmax')
                  xmax.text = str(bounds['max_x'])
                  ymax = ET.SubElement(bndbox, 'ymax')
                  ymax.text = str(bounds['max_y'])

            # Create the XML tree and write it to the output file
            tree = ET.ElementTree(root)
            tree.write(xml_path)

            print(f'Successfully converted {filename} to {xml_filename}')