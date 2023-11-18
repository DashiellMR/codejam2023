import cv2
import pytesseract
import re

def preprocess(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return thresh

cap = cv2.VideoCapture('processed_output.mp4')

numbers_string = ""

for _ in range(10):
    ret, frame = cap.read()
    if not ret:
        break
    
    height, width, _ = frame.shape
    cropped_frame = frame[:height//2, width//2:]
    preprocessed_frame = preprocess(cropped_frame)
    
    text = pytesseract.image_to_string(preprocessed_frame, config='--psm 6 digits')
    text = re.sub(r'\D', '', text)
    numbers_string += text
cap.release()
print(numbers_string)
