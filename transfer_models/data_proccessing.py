import os
import sys
import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.models import Sequential, load_model
from keras import optimizers


class Data_Processing:
    def __init__(self, location: str, file_name: str) -> None:
        """
        :param file_name: name of the file
        :param location: Location where file is stored
        :param dataframe: file opened into dataframe
        :param check_data: checks if the data type is numerical
        :param column_names: list of names of columns in the dataframe
        :param data_type: Data type of the data
        :param save_preTrained_location: location to save sorted dataframe
        :param sorted: If data has been sorted
        :param dataset_usable: This returns True or false whether the data can be used.
        :param save_to_csv: Saved sorted dataframe to a new csv file
        :return: None
        """
        self.location = location
        self.dataframe = self.Load_DataSet()
        self.file_name = file_name.replace(".csv", "") if ".csv" in file_name else file_name
        self.check_data()
        self.column_names = self.columns()
        self.data_type = self.check_type()
        """if self.dataset_usable:
            print("Dataset is useable, please proceed")
        elif self.dataset_usable == None:
            print("A error occured during checking functions for data useability.")
        else:
            print("Dataset return false, please check dataset is a formatted correctly")"""
        self.save_preTrained_location = "/content/drive/My Drive/Colab Notebooks/Dissertation/Tensorflow_DataSets/Sorted_Data/"
        self.sorted = False
        # self.dataset_usable = self.dataset_use_ability
        # if sorted:
        # self.save_to_csv()

    def __str__(self) -> str:
        """
        Prints a description of the class object
        :return: string of Details of object
        """
        if self.data_type == "Numerical":
            return f"Data information:\nLocation: {self.location}\ndata type: {self.data_type}\nfile name: {self.file_name}\nNumber of columns: {len(self.column_names)}\nAmount of rows: {self.dataframe.shape[0]}\n"
        else:
            return f"Data information:\nLocation: {self.location}\ndata type: The columns that are numerical are {self.data_type}\nfile name: {self.file_name}\nNumber of columns: {len(self.column_names)}\nAmount of rows: {self.dataframe.shape[0]}\n"

    def dataset_use_ability() -> bool or None:
        issue_list = []
        try:
            issue_list.append("dataframe" if self.dataframe == None else None)
            issue_list.append("check_type" if self.data_type == None else None)
            issue_list.append("check_data" if self.column_names == None else None)
            isses_list.append("column_names" if self.check_data == None else None)
            if self.check_type or self.check_data or self.column_names or self.dataframe == None:
                print(f"Dataset is usable in this state: Issue with {[x for x in issue_list if x != None]}")
                return False
            else:
                print("No issues have been found")
                return True
        except:
            print("Unknown error: dataset_use_ability")
            return None

    def Load_DataSet(self) -> pd.DataFrame or None:
        """
        Opens the csv file with pandas and is returned a dataframe
        :return: returns data loaded using pandas
        """
        try:
            file = pd.read_csv(self.location)
            return file
        except FileNotFoundError:
            print(f"The file in {self.location} could not be found.")
            return None
        except:
            print("Load_DataSet: Error not accounted for.")
            return None

    def check_type(self, is_numeric: [str] = None) -> str or [str] or None:
        """
        :param is_numeric: True or False if column is numerical in dataframe
        :return: Will return a string if all data is numerical, otherwise will return a list with all the column names that can be used
        """
        try:
            if is_numeric is None:
                is_numeric = []
            for i in range(len(self.column_names)):
                if is_numeric_dtype(self.dataframe[self.column_names[i]]):
                    is_numeric.append(True)
                else:
                    self.convert_string_columns(self.column_names[i])
                    if is_numeric_dtype(self.dataframe[self.column_names[i]]):
                        is_numeric.append(True)
                    else:
                        self.dataframe = self.dataframe.drop(columns=self.column_names[i])
            if all(is_numeric):
                return "Numerical"
            else:
                numerical_list = []
                for is_True in range(len(self.column_names)):
                    if is_numeric[is_True]:
                        numerical_list.append(self.column_names[is_True])
                return numerical_list
        except TypeError:
            # print(f"Check_Type: Type Error: 1:\nShould return  {len(self.column_names)} but returned {len(is_numeric)}.")
            return None
        except ValueError:
            print(f"Check_Type: Value Error: 2:\nIssue is with {print(self)}")
            return None
        except:
            print("Check_Type: Unknown Error: 3: Issue not accounted for.")
            return None

    def save_to_csv(self) -> None:
        """
        Saves the sorted data frame as a new csv
        :return: Doesn't return anything for this
        """
        self.dataframe.to_csv(self.save_preTrained_location + self.file_name + ".csv")

    def show_head(self) -> None:
        if self.data_type == "Numerical":
            print(', '.join(self.column_names))
        elif self.data_type != "Numerical":
            print(', '.join(self.data_type))

    def columns(self, column_names=None) -> [str] or None:
        """
        gets list of column names
        :param column_names: list of column names
        :return: returns a list containing strings
        """
        try:
            if column_names is None:
                column_names = []
            file = pd.read_csv(self.location)
            for column in file.columns:
                column_names.append(column)
            return column_names
        except ValueError:
            print("Value Error 1: function name: columns:")
            return None
        except:
            print("Unknon Error 2: function name: columns:")
            return None

    def convert_string_columns(self, column_to_change: str) -> None:
        unique_values = self.dataframe[column_to_change].unique()
        for index, word in enumerate(unique_values):
            self.dataframe[column_to_change] = self.dataframe[column_to_change].replace([word], index)
        print(f"Converted string's to integer's in {self.file_name}. Column name {column_to_change}")
        print(f"{column_to_change} was {unique_values}")
        print(f"{column_to_change} now {self.dataframe[column_to_change].unique()}")

    def check_data(self) -> pd.DataFrame or None:
        """
        Used to check the data has no NaN/Null's, then will remove them and and will return a new dataframe.
        :return: either the original dataframe or new dataframe containing no null's or returns None
        """
        try:
            if (self.dataframe.isnull().values.ravel().sum()) > 0:
                predict_values()
                print(f"The amount of NaN/Null's in the data is {(self.dataframe.isnull().values.ravel().sum())}")
                dataframe2 = self.dataframe.dropna()
                if (dataframe2.isnull().values.ravel().sum()) == 0:
                    print(f"There are no more NaN/Null's in {self.file_name} in location {self.location}.")
                    return dataframe2
                else:
                    print("There are NaN/Null's that cant be removed this way.\nPlease do it manually.")
                    userinput = input("Would you like to continue: Y or N").upper()
                    if userinput == "Y":
                        self.sorted = True
                        return dataframe2
                    elif userinput == "N":
                        self.sorted = False
                        return None
                    else:
                        print("The option you chose was not in the choice. Default action: stopping")
                        self.sorted = False
                        return None
            else:
                print(f"There are no nulls in the data.")
                self.sorted = True
                return self.dataframe
        except FileNotFoundError:
            print(":File not found:")
            self.sorted = False
            return None
        except TypeError:
            print("Please check the data, there is a type error. ")
            self.sorted = False
            return None
        except:
            print("Check_data: Unknown Error 1:")
            self.sorted = False
            return None

    def predict_values(self):
        print(self.columns)
        print("Correlation: ",
              self.dataframe['points'].corr(df[str(input("Which column do you want to look at for correlation"))]))
        # from here add the n

    def plot_data(self) -> None:
        """
        Plots data with scatter and plot
        :return: Nothing
        """
        while True:
            graph_names = ["scatter", "Box"]
            print("Please choose a plot: ")
            for index, name in enumerate(graph_names):
                print(f"{index}: {name}")
            user_choice = input("Which plotting would like to use: ")
            if user_choice in graph_names:
                if user_choice == "scatter":
                    while True:
                        print("Column names:")
                        self.show_head()
                        X_value = str(input("Which column for X: "))
                        Y_value = str(input("Which column for Y: "))
                        try:
                            if X_value in self.column_names and Y_value in self.column_names:
                                plt.scatter(self.dataframe[X_value], self.dataframe[Y_value])
                                plt.xlabel = X_value
                                plt.ylabel = Y_value
                                plt.show()
                                break
                            else:
                                if X_value in self.column_names:
                                    print(f"{Y_value} is not in the column names. Please try again.")
                                else:
                                    print(f"{X_value} is not in the column names. Please try again.")
                        except TypeError:
                            print("Error 1: Type error")
                        except:
                            print("Error 2: Unknown error")
                elif user_choice == "Box":
                    while True:
                        columns_to_show = []
                        self.show_head()
                        amount_of_columns = int(input("How many columns would you like to use? "))
                        if amount_of_columns <= len(self.column_names):
                            for i in range(amount_of_columns):
                                user_column_selection = input("Enter column name: ")
                                if user_column_selection in self.column_names:
                                    columns_to_show.append(user_column_selection)
                                    i = len(user_column_selection)
                                else:
                                    print("that is not a column in this data")
                            boxplot = self.dataframe.boxplot(column=columns_to_show)
                            plt.show()
                            break
                        else:
                            print("""you have eneterd a number that is larger 
                                      than the amount of columns you have availbe""")
                user_choice = input("Try again: Y or N")
                if user_choice == "Y":
                    continue
                else:
                    break
            else:
                print("The graph you have chosen is not supported.\nPlease try again")


def tensorflow_model(dataset, model: keras.Sequential = None) -> None:
    global pre_trained_model_saves

    data_features = dataset.dataframe.loc[:, dataset.dataframe.columns != "target"]
    data_target = dataset.dataframe.iloc[:, -1]

    X_train, X_test, Y_train, Y_test = train_test_split(data_features, data_target, test_size=0.20)

    print(f"X_train: {X_train.shape}, Y_train shape: {Y_train.shape}")
    print(f"X_test shape: {X_test.shape}, Y_test shape: {Y_test.shape}")

    model = keras.Sequential([
        keras.layers.Dense(64, activation=tf.nn.relu, input_shape=[len(X_train.keys())]),
        keras.layers.Dense(64, activation=tf.nn.relu),
        keras.layers.Dense(1)
    ])
    model.compile(loss='mean_squared_error',
                  optimizer='adam',
                  metrics=['accuracy'])
    model.summary()

    model.fit(X_train, Y_train, epochs=500)
    print("Before transfer learning")
    print(model.evaluate(X_test, Y_test))
    print(model.predict(X_test))
    # model.load_weights(pre_trained_model_saves + "kidney_disease_dataset.h5")
    model.load_weights(pre_trained_model_saves + "Stars.h5")
    print("After transfer learning")
    print(model.evaluate(X_test, Y_test))
    print(model.predict(X_test))


def dataset_random_models(dataset):
    global pre_trained_model_saves
    columns_for_training = str(input("Enter column name: "))
    data_features = dataset.dataframe.loc[:, columns_for_training]
    data_target = dataset.dataframe.iloc[:, -1]
    X_train, X_test, y_train, y_test = train_test_split(data_features,data_target,random_state=23)
    model = keras.Sequential([
                              keras.layers.Dense(64, activation=tf.nn.relu, input_shape=[len(X_train.keys())]),
                              keras.layers.Dense(64, activation=tf.nn.relu),
                              keras.layers.Dense(1)
                              ])
    model.compile(loss='mean_squared_error',
                  optimizer='adam',
                  metrics=['accuracy'])
    model.summary()
    model.fit(X_train,y_train,epochs=500)


    model.save(pre_trained_model_saves + dataset.file_name + ".h5")


def pre_trained_model_check(model_pre_loaded: keras.models.load_model = None) -> None:
    """
    :param model: when the pre trained model is loaded it will be in to this varible which is defined for keras
    :return: Nothing
    """
    global pre_trained_model_saves
    file_list = os.listdir(pre_trained_model_saves)
    print(file_list)
    global object_instance_list
    global dataset_path
    for x in object_instance_list:
        if x.file_name == "heart":
            X_train, X_test, Y_train, Y_test = train_test_split(x.extracted_features, x.extracted_targets,
                                                                test_size=0.20)
    model_TL = load_model(pre_trained_model_saves + "heart.h5")
    model_TL.compile(loss='mean_squared_error', optimizer='adam', metrics=["accuracy"])
    model_TL.summary()
    input("Press enter to continue! ")
    for x in file_list:
        if x != "heart.h5":
            model_TL = load_model(pre_trained_model_saves + x)
            model_TL.summary()
            input("Press enter to continue! ")

    predictions = model_TL.predict(X_test[:3])
    print("predictions shape:", predictions.shape)


class make_pre_trained_Model:
    #################################################Not finished###########################################################
    def __init__(self, object_instance_list, epoch: int = 250, L_R: float = 0.01, layers: int = 2,
                 neurons: [int] = [10, 10]) -> None:
        """
        There are default parameters but can be changed if need be
        :param epoch: number of epoch
        :param L_R: learning rate
        :param layers: layers of the model
        :param neurons: if 3 layers then neurons will be [10,10,10], 10 neurons per layer
        :param data: Data will be loaded a pandas dataframe
        :return: None
        """
        self.epoch = epoch
        self.L_R = L_R
        self.layers = layers
        self.neurons = neurons
        self.data_path = "/content/drive/My Drive/Colab Notebooks/Dissertation/Tensorflow_DataSets/Sorted_Data/"
        self.data_for_NN = self.load_data()

    def __str__(self):
        """
        :return: string containing the parameters of the model
        """
        return f"Epoch: {self.epoch}\nLearning rate: {self.L_R}\nLayers: {self.layers}\nNeurons per layer: {self.neurons}"

    def load_data(self, sorted_data: list = None) -> [str]:
        if sorted_data is None:
            sorted_data = []
        files = os.listdir(self.data_path)
        for file in files:
            data = pd.read_csv(self.data_path + file)
            sorted_data.append(data)
        if len(sorted_data) > 0:
            return sorted_data
        else:
            return None

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivatives(self, x):
        return x * (1 - x)

    for data in object_instance_list:
        data_features = data.dataframe.loc[:, data.dataframe.columns != 'target']
        data_target = data.dataframe.iloc[:, -1]
        X_train, X_test, Y_train, Y_test = train_test_split(data_features, data_target, test_size=0.20, random_state=42)

    def Load_tensorflow_Model():
        pass