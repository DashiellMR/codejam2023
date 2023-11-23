# McGill CodeJam2023: Matrox Challenge 
## We won first place!
I would like to thank Matrox for offering this amazing challenge and I would like to thank my team for allowing me to go off and do this!
## What was the challenge?
The challenge presented to us was: Given an .h264 file
1. Convert the .h264 file to .mp4
2. Remove the salt and pepper noise from the resultant video
3. Extract numbers hidden within the frames of the video
## How did we do it?
The process is pretty simple -- for part one, we utilised ffmpeg, a python library dedicated to video conversions to, well, convert the video. Then, we used a combination of OpenCV's built-in and hand-created matrices to apply different image restoration techniques such as Gaussian Blur, Median Blur, and Sharpening Kernel. For the number extraction, we used pytesseract, a python wrapper for Google's Tesseract Optical Character Recognition engine. However, we ran into some initial difficulties as pytesseract struggled with the vibrant hues of the original video. Because of this, we applied a grayscale filter to each frame, utilise Otsu's Thresholding Algorith, and, finally, cropped the frame to reduce excess, and possibly misinterpretable, symbols. 
## What issues arose throughout?
The majority of the issues came from something unexpected: colorspaces. We spent a solid 15-20 hours just searching for the correct combination of hueshifts and color-inversions, and it ended up not being a necessary part of the challenge.
## What's next?
This project is self-contained, but I would like to utilise the knowledge gained surrounding image processing to create a website that shows the impact that different image kernels have.  
