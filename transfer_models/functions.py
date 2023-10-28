from django.utils import timezone
from pandas.api.types import is_numeric_dtype
import pandas as pd
import tensorflow as tf
import json
from tensorflow import keras
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.models import Sequential, load_model
from keras import optimizers
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
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

def open_file(file, file_type=''):
    if file_type == 'CSV':
        pass
    else:
        return None

def dataframe_to_csv(df, filename):
    if not isinstance(df, pd.DataFrame):
        raise ValueError("df must be a pandas dataframe")
    if not isinstance(filename, str):
        raise ValueError("filename must be a string")
    return df.to_csv(filename, index=False)


def convert_to_numeric_with_one_hot_encoding(series):
    one_hot_encoded_data = pd.get_dummies(series, prefix=series.name)
    label_encoding_dict = {category: i for i, category in enumerate(series.unique())}
    label_encoded_data = series.map(label_encoding_dict).rename(f"{series.name}_label_encoded")
    result = pd.concat([one_hot_encoded_data, label_encoded_data], axis=1)
    return result


def apply_numeric_function(dataframe):
    result = dataframe.apply(convert_to_numeric_with_one_hot_encoding)
    result = pd.concat(result.values, axis=1)
    return result


def predict_missing_values(df, columns_with_missing_values):
    predition = False
    if columns_with_missing_values:
        X = df.drop(columns_with_missing_values, axis=1)
        y = df[columns_with_missing_values]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        print("Mean Squared Error:", mse)
        if y_pred:
            prediction=True
        df.loc[df[column].isnull(), column] = y_pred
        print(df[column].isnull().sum())
    return df, prediction

