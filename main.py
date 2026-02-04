import rembg
from PIL import Image
import io

def remove_background(input_path, output_path):
    with open(input_path, 'rb') as i:
        input_image = i.read()
        output_image = rembg.remove(input_image)
        with open(output_path, 'wb') as o:
            o.write(output_image)

# Example usage for background removal
# remove_background('input.jpg', 'output.png')