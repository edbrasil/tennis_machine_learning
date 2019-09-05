# -*- coding: utf-8 -*-
"""
Created on Mon Dec  10 13:33:53 2018

@author: edbras
"""
"""
Use 4 training tournaments (508 matches) to train
a neural network
"""

# Import necessary modules
from data_prep import data_prep_func
import numpy as np
np.random.seed(100)
import keras
from keras.layers import Dense
from keras.layers import Dropout
from keras.models import Sequential
from keras.utils import to_categorical
from keras.callbacks import EarlyStopping
#from keras.models import load_model
import pandas as pd
#from sklearn.externals import joblib
import joblib
import matplotlib.pyplot as plt

tourn_list = ['U2016','A2017','F2017','W2017','U2017','A2018','F2018','W2018','U2018','A2019','F2019','W2019']
df_list = []

for f in tourn_list:
    df_list.append(pd.read_excel('./data/data_'+f+'.xls', header = 0, index_col = 0))

df_train = pd.concat(df_list, ignore_index = True)

#def NeuNetTennis(df_train):
X_train, y_train = data_prep_func(df_train, full_data=True, drop_extra = True)
y_train = to_categorical(y_train)
X_list = list(X_train.columns.values)
joblib.dump(X_list, "X_list_neunet.save")

# Specify the model
n_cols = X_train.shape[1]

keras.backend.clear_session()
model = Sequential()
num_nodes = 50
model.add(Dense(num_nodes, activation='relu', input_shape = (n_cols,)))
model.add(Dropout(0.3))
model.add(Dense(num_nodes, activation='relu'))
model.add(Dropout(0.3))
#model.add(Dense(num_nodes, activation='relu'))
#model.add(Dense(num_nodes, activation='relu'))
model.add(Dense(2,activation='sigmoid'))

model.compile(optimizer='adam',loss='categorical_crossentropy'
              ,metrics=['accuracy'])

early_stopping_monitor = EarlyStopping(patience=4)
result = model.fit(X_train, y_train, epochs=50
          ,validation_split = 0.3, callbacks=[early_stopping_monitor])

# Create the plot
plt.plot(result.history['val_loss'], 'r', result.history['val_acc'],'b')
plt.xlabel('Epochs')
plt.ylabel('Validation score')
plt.show()

#Save model
model.save('model_50_2.h5')

#prediction test
#from getData_Full import wrapper
#model = load_model('model_10_1.h5')
#p_dict = {'r4': ['N Djokovic','JM del Potro']}
#wrapper(p_dict, type = 'dict', out_file = '_temp.xls',
#    tourn = 'US', court = 'H', rd = 'r4',all_rounds = False) 
#
#df_t = pd.read_excel('_temp.xls', header = 0, index_col = 0)
#
##global X_test
#X_test, y_test = data_prep_func(df_t, X_list, full_data=False, drop_extra=True)
#
#y_pred = model.predict(X_test)
#print(y_pred)
#print(np.rint(y_pred))
#y_pred predicts whether player 0 wins (1) or not (0)
#therefore return (1- y_pred ) to decide which player wins


