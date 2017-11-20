#!/bin/python

from skimage.io import imread, imshow
from matplotlib import pyplot as plt
from skimage.color import rgb2grey
from skimage.transform import resize

# Teacher-provided hash function
def compute_hash(differences):
    total_string = []
    for difference in differences:
        decimal_value = 0
        hex_string = []
        for index, value in enumerate(difference):
            if value:
                decimal_value += 2**(index % 8)
            if (index % 8) == 7:
                hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))
                decimal_value = 0
    
        total_string.append(*hex_string)
    return ''.join(total_string)


# Read two different closely-related images 
img1 = imread('cat_reference.png')
img2 = imread('cat_eye.png')
# Read a very different image
img3 = imread('stickman.png')

# Convert the pictures to grey-scale
greyscale_img1 = rgb2grey(img1)
greyscale_img2 = rgb2grey(img2)
greyscale_img3 = rgb2grey(img3)

# Resize the pictures in 9x8
resized_img1 = resize(greyscale_img1, (9,8))
resized_img2 = resize(greyscale_img2, (9,8))
resized_img3 = resize(greyscale_img3, (9,8))

# Compute the difference matrix
differences = resized_img1 > resized_img2
print(
    'Hash of reference/closely-related to reference pictures is {}.'
    .format(compute_hash(differences))
)
differences = resized_img1 > resized_img3
print(
    'Hash of reference/unrelated to reference pictures is {}.'
    .format(compute_hash(differences))
)
