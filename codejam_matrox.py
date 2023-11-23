import ffmpeg
import cv2
import skvideo.io
import skvideo.datasets
import numpy as np
import pytesseract
import re
import time

t1 = time.time() # Grab start time

#Step 1: Convert .h264 to .mp4
input_stream = ffmpeg.input('codejam_matrox_2023_noisy.h264') # Initialise input video
ffmpeg.output(input_stream, 'output.mp4').run() # Convert image to .mp4 file

#Step 2: Remove noise and fix colour
cap = cv2.VideoCapture('output.mp4') # Take the newly outputted video and set is as the source

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) # Retrieve video width
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) # Retrieve video height
fps = cap.get(cv2.CAP_PROP_FPS) #Retrieve video FPS
fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Identify desired data format (in this case an .mp4v)

out = cv2.VideoWriter('complete.mp4', fourcc, fps, (frame_width, frame_height)) # Indicate characteristics of the output

blur_kernel = np.array([[0.0625, 0.125, 0.0625],[0.125, 0.25, 0.125],[0.0625, 0.125, 0.0625]]) # 3x3 Gaussian Blur
sharpening_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]) # 3x3 Sharpening Kernel

while True:
    ret, frame = cap.read() # Read frame
    if not ret: # Check if there are no frames remaining
        break
    
    filtered_frame = cv2.medianBlur(frame, 3) # Built-in 3x3 Median Blur
    blur_frame = cv2.filter2D(filtered_frame, -1, blur_kernel) # Apply Gaussian Blur
    sharpened_frame = cv2.filter2D(blur_frame, -1, sharpening_kernel) # Apply Sharpening Kernel
    
    out.write(sharpened_frame) # Output newly modified frame
    
cap.release() # Don't forget to release !
out.release() # Don't forget to release x2 !

cap = cv2.VideoCapture('complete.mp4') # Output filename

#Step 3: Extract the numbers
numbers = "" # Initialise string to hold video numbers
 
def preprocess(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Convert to grayscale
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU) # Apply Otsu's Thresholding Algorithm (Dynamic Thresholding)
    return thresh 

for _ in range(8): 
    ret, frame = cap.read() # Read frame
    if not ret: # Check if there are any frames left
        break
    
    height, width, _ = frame.shape # Define size of the frame
    
    cropped_frame = frame[:height//3, width//2:] # Crop frame to assist in number transcription
    
    preprocessed_frame = preprocess(cropped_frame) # Apply thresholding to current frame
    
    text = pytesseract.image_to_string(preprocessed_frame, config='--psm 6 digits') # Extract number from frame
    text = re.sub(r'\D', '', text) # Remove noise from transcription

    numbers += text # Add current number
    
cap.release() # Don't forget to release x3 !
t2 = time.time() # Grab finish time
print(f"String Found: {numbers}, Time Taken: {round(t2-t1, 3)}s") # Print out transcribed numbers and time taken to complete
