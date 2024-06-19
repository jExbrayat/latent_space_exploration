import json
import numpy as np
from PIL import Image
import io

# Load meshgrid
with open("assets/decoded_meshgrid.json", "r") as file:
    decoded_meshgrid = json.load(file)

# Create a list to store image bytes
image_bytes_list = []

for img_idx in range(len(decoded_meshgrid)):  # Iterate over images of shape (784,)
    img = np.array(decoded_meshgrid[img_idx])  # Convert as np array
    img = img.reshape(28, 28)

    pil_img = Image.fromarray(img)  # Convert as pillow object
    compressed_img = pil_img.convert("L")  # Convert to 8-bit pixels, grayscale

    # Save image bytes to list
    with io.BytesIO() as output:
        compressed_img.save(output, format="PNG")
        img_bytes = output.getvalue()
        image_bytes_list.append(img_bytes)


# Write all image bytes to a binary file
with open("assets/decoded_meshgrid.bin", "wb") as binary_file:
    for img_bytes in image_bytes_list:
        binary_file.write(img_bytes)

# Here is how bytes sequences of different images are separated
for img in image_bytes_list[:10]:
    header = [byte for byte in img[:4]]
    converted_header = bytes(header)
    print(header)
    print(converted_header)
