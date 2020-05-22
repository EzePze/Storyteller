from __future__ import print_function
from keras.callbacks import LambdaCallback
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.layers import RNN
from keras.utils import np_utils
import keras
import numpy as np
import random
import sys
import os
import hashlib
import generator
import re

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

def read_data(file_name):
    #open and read text file
    text = open(file_name, encoding='utf-8').read()
    return text

def on_epoch_end(epoch, _):
    # Function invoked at end of each epoch. Prints generated text.

    print("saving model")
    model.save(chosen_model + "Model.h5")

    print()
    #print('----- Generating text after Epoch: %d' % epoch)

    #generateText()

def get_model_selection():
    print("Select a model or create a new one:\n\n[0] New Model\n[1] Delete Model")
    for i in model_dict:
        print('[%d] %s' % (i, model_dict[i].title()))

    print()
    model_select = int(input())
    print()
    return model_select

def update_dict(list = 'ListOfModels.txt'):
    data = read_data(list).lower()
    return dict((i,c) for i,c in enumerate(data.split(), 2))

def create_model(name, data):
    with open('ListOfModels.txt', 'a') as modelList:
        modelList.write(name + '\n')
    with open('%s.txt' % name, 'w') as newData:
        newData.write(read_data(data))
    print('\nCreated model \'%s\'\n' % name)

def delete_model(name):
    oldList = read_data('ListOfModels.txt').lower()
    oldList = oldList.replace(name,'')
    with open('ListOfModels.txt', 'w') as newList:
        newList.write(oldList)
    if os.path.isfile(name + "Model.h5"):
        os.remove('%sModel.h5' % name)
    if os.path.isfile(name + ".txt"):
        os.remove('%s.txt' % name)
    print('Deleted model \'%s\'\n' % name)


print("  _________ __                       ___________    .__  .__                ")
print(" /   _____//  |_  ___________ ___.__.\__    ___/___ |  | |  |   ___________ ")
print(" \_____  \    __\/  _ \_  __ \   |  |  |    |_/ __ \|  | |  | _/ __ \_  __ \ ")
print(" /        \|  | (  (_) |  | \/\___  |  |    |\  ___/|  |_|  |_\  ___/|  | \/")
print("/_______  /|__|  \____/|__|   /_____|  |____| \___  |____/____/\___  |__|   ")
print("        \/                    \/                  \/               \/       ")
print("")
print("")
print("")

#credentials = read_data("login.txt")
#rows = credentials.split("\n")
#login = False

#while not login:
#    i = 0
 #   user = input("Username: ").lower()
  #  password = input("Password: ").lower()

   # while not login and i < len(rows) - 1:

    #    compare = rows[i].split(', ')
     #   if user == compare[0] and hashlib.sha256(str.encode(password)).hexdigest() == compare[1]:
      #      login = True
       # i += 1

    #if not login:
     #   print("Invalid login. Try again.\n")

#print("Login successful. Welcome, %s.\n" %user)
while True:
    model_dict = update_dict()
    model_select = get_model_selection()

    while model_select not in range(2, len(model_dict) + 2):
        if not model_select:
            name = input('\nEnter the name for your new model: ').lower()
            data = input('\nEnter the name of the text file to be used for modelling (needs to be in the /Storyteller folder): ')
            while not os.path.isfile(data):
                print('\nInvalid file. Are you sure the file \'%s\' is in the /Storyteller folder?\n' % data)
                data = input('\nEnter the name of the text file to be used for modelling (needs to be in the /Storyteller folder): ')
            create_model(name, data)
            model_dict = update_dict()
            model_select = get_model_selection()

        elif model_select == 1:
            print('\nWhich model do you wish to delete?\n')
            for i in model_dict:
                print('[%d] %s' % (i - 2, model_dict[i].title()))
            print()
            name = int(input())
            if input('Are you sure you wish to delete model \'%s\'? (y/n)\n\n' % model_dict[name + 2]) == 'y':
                print()
                delete_model(model_dict[name + 2])
                model_dict = update_dict()
                print('\nReturning to model selection screen...\n\n')
            else:
                print('Cancelling...\n\nReturning to model selection...\n')
            model_select = get_model_selection()
        
        else:
            print('Please choose a number in the provided range\n')
            model_select = get_model_selection()


    chosen_model = model_dict[model_select]

    custom = (input("""Select a mode:

[1] Use custom input 
[2] Use sentence from the model text file

""") == "1")

    text = read_data(chosen_model + ".txt")
    length = len(text)
    sentences = re.split('(?<=[\.!\?]) ', text.replace('\n', ' '))
    raw_text = sentences[random.randint(0,len(sentences) - 1)]

    # load the model: a single LSTM
    print("loading model %s" % (chosen_model))
    print("")
    print("------------------------------------------------------")

    #if not os.path.isfile(chosen_model + "Model.h5"):
        #model = keras.Sequential()
        #model.add(keras.layers.LSTM(128, input_shape=(maxlen, len(chars))))
        #model.add(keras.layers.Dense(len(chars), activation='softmax'))

        #model.compile(loss='categorical_crossentropy', optimizer=optimizer)

    generator.interact_model(custom, raw_text)


