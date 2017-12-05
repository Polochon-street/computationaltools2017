#!/bin/python

from moviepy.editor import *
import numpy as np
import os
import shelve
from skimage.color import rgb2grey
from skimage.transform import resize
from sklearn.cluster import KMeans
from adjusted_rand_index import rand_index

# This was the hashing function used in week11 by the teacher
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


def compute_mean(video):
    """
        Compute the mean of all video's frames.

        :param video: video filename (str)
        :param output: the computed mean (float)
    """
    # Open the video file
    video = VideoFileClip(video)

    # Ready the final mean array
    mean = np.zeros([9, 8])

    # Iterate through the video frames
    for i,frame in enumerate(video.iter_frames()):
        # Convert the frame to greyscale
        greyscale_frame = rgb2grey(frame)
        # Resize the image to be 9x8
        resized_img = resize(greyscale_frame, (9, 8))
        # Increase the mean by the result
        mean += resized_img

    # Compute the mean by dividing the sum of the frames by their numbers
    mean = mean / (i+1)
    return mean

# Make a list of all video files
videos = [ '/'.join(['videos', f]) for f in os.listdir('videos')]

# Open video_dict as a shelve (e.g. a persistent dict)
with shelve.open('video_hash') as video_dict:
    # For each video
    for a, video in enumerate(videos):
        # Compute the mean of all frames
        mean = compute_mean(video)
        # Compute the video's hash using the mean array
        difference = np.zeros([8,8])
        for i in range(0, 8):
            difference[i] = mean[i] > mean[i+1]
        hsh = compute_hash(difference)
        # Convert the hash from a string to an array of hex figures 
        # like this: [0xd, 2, 0xf, ...]
        hsh = np.array([int(x, 16) for x in hsh])
        # Store the video's hash in the dict
        video_dict[video] = hsh

    # Start the clustering

    # Make a list of all videos coordinates
    X = np.array(list(video_dict.values()))
    # Make a list of the videos names formatted like in the rand_index file
    H = [(x.split('/')[1]).split('.')[0] for x in video_dict.keys()]
    # Cluster them using the KMeans method
    kmeans = KMeans(n_clusters=970, random_state=0).fit(X)
    # Get the corresponding labels
    labels = kmeans.labels_

    # Allocate memory for the final cluster variable
    clusters = []
    for i in range(0,970):
        clusters.append(set())

    # Do the actual clustering
    for i,label in enumerate(labels):
        clusters[label].add(H[i])

    # Compute the final accuracy score
    score = rand_index(clusters)
    print('Rand-index is {}'.format(score))
