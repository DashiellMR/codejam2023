import ffmpeg
import cv2
import skvideo.io
import skvideo.datasets
import numpy as np

#step 1: convert video to .mp4
#input_stream = ffmpeg.input('codejam_matrox_2023_noisy.h264')
#ffmpeg.output(input_stream, 'output.mp4').run()

#step 2: remove noise and fix colour
def correct_yellowish_tint(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL)

    hue_shift = 260 
    saturation_shift = 0
    value_shift = 0  

    hsv[:, :, 0] = (hsv[:, :, 0] + hue_shift) % 180  # Hue shift
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] + saturation_shift, 0, 255)  # Saturation shift
    hsv[:, :, 2] = np.clip(hsv[:, :, 2] + value_shift, 0, 255)  # Value shift

    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR_FULL)

cap = cv2.VideoCapture('output.mp4')

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

out = cv2.VideoWriter('processed_output.mp4', fourcc, fps, (frame_width, frame_height))

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

print("Done")