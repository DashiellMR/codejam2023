import cv2
import numpy as np

# Function to convert frame to grayscale and adjust brightness
def convert_to_grayscale_and_adjust_brightness(frame, brightness=0):
    # Apply median blur to reduce noise
    frame = cv2.medianBlur(frame, 5)
    # Apply sharpening filter
    sharpen_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    frame = cv2.filter2D(frame, -1, sharpen_kernel)
    # Convert to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Adjust brightness
    if brightness != 0:
        # Create an array of brightness values
        brightness_array = np.full(gray_frame.shape, brightness, dtype=np.uint8)
        if brightness > 0:
            gray_frame = cv2.add(gray_frame, brightness_array)
        else:
            gray_frame = cv2.subtract(gray_frame, brightness_array)
    return gray_frame

brightness_change = 0  # Increase or decrease this value to adjust brightness

cap = cv2.VideoCapture('output.mp4')

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

# Initialize VideoWriter for grayscale output
out = cv2.VideoWriter('processed_output.mp4', fourcc, fps, (frame_width, frame_height), isColor=False)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Process the frame and convert it to grayscale and adjust brightness
    gray_and_bright_frame = convert_to_grayscale_and_adjust_brightness(frame, brightness_change)

    # Write the grayscale and brightness adjusted frame to the output video
    out.write(gray_and_bright_frame)

# Release the VideoCapture and VideoWriter objects
cap.release()
out.release()
