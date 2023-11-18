import cv2
import numpy as np

# Function to calculate the shift needed
def calculate_shift(original, modified):
    # Calculate the difference
    difference = original - modified
    # Adjust for the circular nature of the hue channel
    difference[difference > 90] -= 180
    difference[difference < -90] += 180
    return np.mean(difference), np.median(difference)

# Function to apply the calculated shift
def apply_shift(image, shift, channel):
    if channel == 0:  # Hue channel
        image[:, :, channel] = (image[:, :, channel] + shift) % 180
    else:  # Saturation and value channels
        image[:, :, channel] = np.clip(image[:, :, channel] + shift, 0, 255)
    return image

# Load the images
original = cv2.imread('original.png')  # Update with the correct path
messed_up = cv2.imread('messed_up.png')  # Update with the correct path

# Ensure the images are the same size
if original.shape != messed_up.shape:
    messed_up = cv2.resize(messed_up, (original.shape[1], original.shape[0]))

# Convert to HSV
hsv_original = cv2.cvtColor(original, cv2.COLOR_BGR2HSV)
hsv_messed_up = cv2.cvtColor(messed_up, cv2.COLOR_BGR2HSV)

# Calculate shifts needed for each channel
hue_shift, _ = calculate_shift(hsv_original[:, :, 0], hsv_messed_up[:, :, 0])
saturation_shift, _ = calculate_shift(hsv_original[:, :, 1], hsv_messed_up[:, :, 1])
value_shift, _ = calculate_shift(hsv_original[:, :, 2], hsv_messed_up[:, :, 2])

# Apply the shifts
hsv_messed_up = apply_shift(hsv_messed_up, hue_shift, 0)
hsv_messed_up = apply_shift(hsv_messed_up, saturation_shift, 1)
hsv_messed_up = apply_shift(hsv_messed_up, value_shift, 2)

# Convert back to BGR
corrected_image = cv2.cvtColor(hsv_messed_up, cv2.COLOR_HSV2BGR)

# Save the corrected image
cv2.imwrite('corrected_image.png', corrected_image)  # Update with the correct path
