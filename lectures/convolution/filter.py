import math
import sys

from PIL import Image, ImageFilter

# Ensure correct usage
if len(sys.argv) != 2:
    sys.exit("Usage: python filter.py imagename")

# Open image
image = Image.open(sys.argv[1]).convert("RGB")

# Filter image based on edge detection kernel
filtered = image.filter( ImageFilter.Kernel(
    size = (3,3),
    kernel=[-1, -1, -1, -1, 8, -1, -1, -1, -1],
    scale = 1
))

#Show resulting image
filtered.show()
