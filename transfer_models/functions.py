from django.utils import timezone
from pandas.api.types import is_numeric_dtype
import pandas as pd
import tensorflow as tf
import json
from tensorflow import keras
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.models import Sequential, load_model
from keras import optimizers
import os
import sys
import matplotlib.pyplot as plt
from .models import *
import os
from pandas.api.types import is_numeric_dtype
import logging
import csv

log = logging.getLogger(__name__)
def logging(operation, function, log_type, comment):
  #template for usign logger - use 1 if log for when program running, and 0 for errors.
  #logging(operation="0", function="ERROR", log_type="CreateModel.check_file", comment="No file found")
  return log.debug(f"{operation}: {log_type} - Function: {function} - {comment}")

def get_columns(data):
    lines = data.readlines()
    line = lines[0]
    line = str(line, 'utf-8')
    return line

def get_count(data):
    if type(data) is list:
        return len(data)
    elif type(data) is type('str'):
        return len(data.split(","))
    else:
        return ''


def file_extension(file):
    extensions = ['csv', 'png', 'jpg']
    split = os.path.splitext(file)
    return split[1] if split[1] in extensions else None


def save_as_pretrained_model(model):
    return model.save('pre-trained_model.h5')

def export_csv(data):
    df = pd.read_csv(data)
    return df

def exporter(model, data):
    csv = export_csv(data)
    modelh5 = save_as_pretrained_model(model)
    return csv, modelh5


def Detect_Filetype(data):
    columns = data.columns.values.tolist()
    for column in columns:
        if not is_numeric_dtype(data[column]):
            return 'Assorted'
            break
    return 'Numerical'

















