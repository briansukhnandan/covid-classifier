import PIL
import os
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image

import numpy as np
from tqdm import tqdm
from sklearn.model_selection import train_test_split

from tensorflow.keras.models import Sequential
from sklearn.metrics import classification_report, confusion_matrix
from tqdm import tqdm
from sklearn.model_selection import train_test_split
import tensorflow.keras.layers as Layers

import seaborn as sns
import matplotlib.pyplot as plt

def run_model_prediction(filename):

    model = tf.keras.models.load_model('../saved_model/model')
    os.remove("image.jpg")

    t_a = []

    img = image.load_img(filename, target_size=(127,127))
    img = image.img_to_array(img) / 255
    t_a.append(img)
    single_img_pred = (model.predict(np.array(t_a)) > 0.5).astype("int32")

    class_chosen = single_img_pred[0][0]

    outcomes = {
        0 : "Not COVID",
        1 : "COVID"
    }


    return outcomes[ class_chosen ]