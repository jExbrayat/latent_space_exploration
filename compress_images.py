import json
import numpy as np

from PIL import Image

# Load meshgrid
with open("assets/decoded_meshgrid.json", "r") as file:
    decoded_meshgrid = json.load(file)

for img_idx in range(len(decoded_meshgrid)):  # Iterate over images of shape (784,)

    img = np.array(decoded_meshgrid[img_idx])  # Convert as np array
    img = img.reshape(28, 28)

    pil_img = Image.fromarray(img)  # Convert as pillow object
    compressed_img = pil_img.convert("L")  # Convert to 8-bit pixels, grayscale

    compressed_img.save(f"imgs/decoded_meshgrid_{img_idx}.png")
