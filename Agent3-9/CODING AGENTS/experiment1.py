# ************************************************
# ************************************************
# ************ File name: experiment1.py *********
# ************************************************
# ************************************************

import cv2
import numpy as np
import matplotlib.pyplot as plt

# ---- Clear environment equivalents ----
# (Not needed in Python; restarting script clears memory automatically)

# ---- Read the colour image ----
myimage = cv2.imread('yellow.jpeg')  # OpenCV reads in BGR format
if myimage is None:
    raise FileNotFoundError("Image 'yellow.jpeg' not found in the working directory.")

# ---- Resize to 256 x 256 ----
mycolorimage = cv2.resize(myimage, (256, 256), interpolation=cv2.INTER_NEAREST)

# ---- Convert to grayscale ----
mygrayimage = cv2.cvtColor(mycolorimage, cv2.COLOR_BGR2GRAY)

# ---- Convert to binary (thresholding) ----
# Equivalent of im2bw in MATLAB: simple threshold at 128
_, mybinimage = cv2.threshold(mygrayimage, 128, 255, cv2.THRESH_BINARY)

# ---- Display in a 2x2 grid ----
plt.figure(figsize=(8, 8))

# Original color image (convert BGR to RGB for matplotlib)
plt.subplot(2, 2, 1)
plt.imshow(cv2.cvtColor(mycolorimage, cv2.COLOR_BGR2RGB))
plt.title('Original Colour Image')
plt.axis('off')

# Grayscale image
plt.subplot(2, 2, 2)
plt.imshow(mygrayimage, cmap='gray')
plt.title('Grey Image')
plt.axis('off')

# Binary image
plt.subplot(2, 2, 3)
plt.imshow(mybinimage, cmap='gray')
plt.title('Binary Image')
plt.axis('off')


# ---- Line Profile (like improfile in MATLAB) ----
def line_profile(image, x1, y1, x2, y2, num_points=100):
    """
    Sample intensity values along a line between (x1,y1) and (x2,y2).
    image must be grayscale.
    """
    # Generate equally spaced coordinates along the line
    x, y = np.linspace(x1, x2, num_points), np.linspace(y1, y2, num_points)
    # Use bilinear interpolation of pixel values
    values = image[y.astype(np.int32), x.astype(np.int32)]
    return values

# Coordinates: (10,45) to (50,100)
profile = line_profile(mygrayimage, 10, 45, 50, 100)

plt.subplot(2, 2, 4)
plt.plot(profile)
plt.xlabel('Distance')
plt.ylabel('Pixel Value')
plt.title('Intensity profile of the given line')

plt.tight_layout()
plt.show()
