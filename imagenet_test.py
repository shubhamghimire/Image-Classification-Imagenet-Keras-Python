# Reference Article URL: https://www.pyimagesearch.com/2016/08/10/imagenet-classification-with-python-and-keras/

# import the necessary packages
from keras.preprocessing import image as image_utils
from keras.applications.imagenet_utils import decode_predictions
from keras.applications.imagenet_utils import preprocess_input
from keras.applications import VGG16
import numpy as np
import argparse
import cv2

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to the input image")
ap.add_argument("-o", "--output", type=str, help="path to output image")
args = vars(ap.parse_args())

# load the original image via OpenCV so we can draw on it and display it to our screen later
orig = cv2.imread(args["image"])


# load the input image using the Keras helper utility shile ensuring that the image
# is resized to 224x224 pixels, the required input dimensions for the network -- then
# convert the PIL image to a Numpy array

print("[INFO] loading and preprocessing image....")
image = image_utils.load_img(args["image"], target_size=(224, 224))
image = image_utils.img_to_array(image)

# our image is now represented by a NumPy array of shape (224, 224, 3),
# assuming Tensorflow "channels last" ordering of course, but we need
# to expand the dimensions to be (1, 3, 224, 224) so we can pass it
# through the network -- we'll also preprocess the image by subtracting
# the mean RGB pixel intensity from the ImageNet dataset

image = np.expand_dims(image, axis=0)
image = preprocess_input(image)


# load the VGG16 network pre-trained on the ImageNet dataset
print("[INFO] loading network...")
model = VGG16(weights="imagenet")

# calssify the image
print("[INFO] classifying image...")
preds = model.predict(image)
P = decode_predictions(preds)

# loop over the predictions and display the rank-5 predictions +
# probabilities to our terminal

for (i, (imagenetID, label, prob)) in enumerate(P[0]):
    print("{}. {}: {:.2f}%".format(i+1, label, prob * 100))

# load the image via OpenCV, draw the top prediction on the image,
# and display the image to our screen
orig = cv2.imread(args["image"])


# Percentage by which the image is resized
scale_percent = 75

# Calculate the 75 percent of original dimensions
width = int(orig.shape[1] * scale_percent / 100)
height = int(orig.shape[0] * scale_percent / 100)
dsize = (width, height)

# resize image
orig = cv2.resize(orig, dsize)

(imagenetID, label, prob) = P[0][0]

# draw the predicted name on the image
cv2.putText(orig, "Label: {}, {:.2f}%".format(label, prob * 100),
            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

# Saving the image if the output argument is passed
if args["output"]:
    cv2.imwrite(args["output"], orig)

# Showing the image
cv2.imshow("Classification", orig)
cv2.waitKey(0)
