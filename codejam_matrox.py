import ffmpeg
import cv2
import skvideo.io
import skvideo.datasets
import numpy as np
import pytesseract

#Step 1: convert .h264 to .mp4
input_stream = ffmpeg.input('codejam_matrox_2023_noisy.h264')
ffmpeg.output(input_stream, 'output.mp4').run()

#Step 2: remove noise and fix colour
def correct_yellowish_tint(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    hue_shift = -20
    saturation_shift = 0
    value_shift = 0 

    hsv[:, :, 0] = (hsv[:, :, 0] + hue_shift) % 180
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] + saturation_shift, 0, 255)
    hsv[:, :, 2] = np.clip(hsv[:, :, 2] + value_shift, 0, 255)

    corrected_hsv = np.clip(hsv, 0, 255)
    corrected_frame = cv2.cvtColor(corrected_hsv, cv2.COLOR_HSV2BGR)

    return corrected_frame

cap = cv2.VideoCapture('output.mp4')

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

out = cv2.VideoWriter('complete.mp4', fourcc, fps, (frame_width, frame_height))

shrp_kernel_2 = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])

while True:
    ret, frame = cap.read()
    if not ret:
        break

    filtered_frame = cv2.medianBlur(frame, 5)

    sharpened_frame = cv2.filter2D(filtered_frame, -1, shrp_kernel_2)

    corrected_frame = correct_yellowish_tint(sharpened_frame)

    out.write(corrected_frame)

cap.release()
out.release()

def preprocess_for_ocr(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return thresh

cap = cv2.VideoCapture('complete.mp4')

numbers_string = ""

for _ in range(10):
    ret, frame = cap.read()
    if not ret:
        break
    
    height, width, _ = frame.shape
    
    cropped_frame = frame[:height//2, width//2:]
    
    preprocessed_frame = preprocess_for_ocr(cropped_frame)
    
    text = pytesseract.image_to_string(preprocessed_frame, config='--psm 6 digits')
    text = re.sub(r'\D', '', text)

    numbers_string += text
    
cap.release()
print(numbers_string)
print("Done")