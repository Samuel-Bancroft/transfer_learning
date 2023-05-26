from django.utils import timezone
from pandas.api.types import is_numeric_dtype
import tensorflow as tf
from tensorflow import keras
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.models import Sequential, load_model
from keras import optimizers
import os
import sys
import matplotlib.pyplot as plt
from .models import *

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

def check_file(obj, is_numeric=[], csv_file=None, count=0):
    if not csv_file:
        csv_file = pd.read_csv(obj.file)
    if csv_file.isnull().values.ravel().sum() > 0:
        csv_file_dropna = csv_file.dropna()
        if count <= 3:
            count+=1
            check_file(obj=obj, csv_file=csv_file, count=count)
        else:
            return 'ERROR: File cant be used, please retry with another csv file'
    else:
        columns = obj.column_name_list()
        for column in columns:
            if is_numeric_dtype(csv_file[column]):
                is_numeric.append(True)
            else:
                unique_values = csv_file[column].unique()
                for index, word in enumerate(unique_values):
                    csv_file[column] = csv_file[column].replace([word], index)
                if is_numeric_dtype(csv_file[column]):
                    is_numeric.append(True)
                else:
                    csv_file = csv_file.drop(columns=column)
        if all(is_numeric):
            pass
        else:
            pass

    return ''



