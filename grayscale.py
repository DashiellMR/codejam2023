import cv2

# Load the image from file
image = cv2.imread('original.png')

# Convert the image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Save the grayscale image to file
cv2.imwrite('grayscale_image.jpg', gray_image)
