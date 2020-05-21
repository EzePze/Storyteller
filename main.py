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
import fire

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

def read_data(file_name):
    #open and read text file
    text = open(file_name, encoding='utf-8').read()
    return text.lower()

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
    data = read_data(list)
    return dict((i,c) for i,c in enumerate(data.split(), 2))

def create_model(name, data):
    with open('ListOfModels.txt', 'a') as modelList:
        modelList.write(name + '\n')
    with open('%s.txt' % name, 'w') as newData:
        newData.write(read_data(data))
    print('\nCreated model \'%s\'\n' % name)

def delete_model(name):
    oldList = read_data('ListOfModels.txt')
    oldList = oldList.replace(name,'')
    with open('ListOfModels.txt', 'w') as newList:
        newList.write(oldList)
    if os.path.isfile(name + "Model.h5"):
        os.remove('%sModel.h5' % name)
    if os.path.isfile(name + ".txt"):
        os.remove('%s.txt' % name)
    print('Deleted model \'%s\'\n' % name)

# def sample(preds, temperature=1.0):
#     # helper function to sample an index from a probability array
#     preds = np.asarray(preds).astype('float64')
#     preds = np.log(preds) / temperature
#     exp_preds = np.exp(preds)
#     preds = exp_preds / np.sum(exp_preds)
#     probas = np.random.multinomial(1, preds, 1)
#     return np.argmax(probas)

# def generateText():
#     start_index = random.randint(0, len(text) - maxlen - 1)
#     sentence = input('\nEnter an opening sentence: ').lower() if input('''[1] Enter custom input
# [2] Use sentence from training data\n\n''') == '1' else text[start_index: start_index + maxlen]
#     print('----- Generating with seed: "' + sentence + '"')
#     for diversity in [0.2, 0.5, 1.0, 1.2]:
#         print("""
#         """)
#         print('----- Diversity:', diversity)
#         print(""" """)

#         generated = ''
#         print("""
#         """)
#         generated += sentence
#         sys.stdout.write(generated)

#         for i in range(400):
#             x_pred = np.zeros((len(chars), maxlen, 1))
#             for t, char in enumerate(sentence):
#                 x_pred[t, 0, char_indices[char]] = 1.

#             preds = model.predict(x_pred, verbose=0)[0]
#             next_index = sample(preds, diversity)
#             next_char = indices_char[next_index]

#             sentence = sentence[1:] + next_char

#             sys.stdout.write(next_char)
#             sys.stdout.flush()
#         print()

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
model_dict = update_dict()
model_select = get_model_selection()

while model_select not in range(2, len(model_dict) + 2):
    if not model_select:
        name = input('\nEnter the name for your new model: ').lower()
        data = input('\nEnter the name of the text file to be used for training (needs to be in the /Storyteller folder): ')
        while not os.path.isfile(data):
            print('\nInvalid training data. Are you sure the file \'%s\' is in the /Storyteller folder?\n' % data)
            data = input('\nEnter the name of the text file to be used for training (needs to be in the /Storyteller folder): ')
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

train = (input("""Select a mode:

[1]Train the model
[2]Generate text with the model

""") == "1")


text = read_data(chosen_model + ".txt")

chars = sorted(list(set(text)))
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

# cut the text in semi-redundant sequences of maxlen characters
maxlen = 100

if chosen_model == 'general':
    step = 30000
elif chosen_model == 'nietzsche':
    step = 1
elif chosen_model == 'shakespeare':
    step = 1

length = len(text)

X = []
Y = []

for i in range(0, length-maxlen, 1):
    sequence = text[i:i + maxlen]
    label = text[i + maxlen]
    X.append([char_indices[char] for char in sequence])
    Y.append(char_indices[label])

X_modified = np.reshape(X, (len(X), maxlen, 1))
X_modified = X_modified / float(len(chars))
Y_modified = np_utils.to_categorical(Y)

if train:
    print('Training data length:', len(text))
    print('Total unique characters:', len(chars))
    print('')
    print('Vectorization...')

# load the model: a single LSTM
print("loading model %s" % (chosen_model))
print("")
print("------------------------------------------------------")

#if not os.path.isfile(chosen_model + "Model.h5"):
    #model = keras.Sequential()
    #model.add(keras.layers.LSTM(128, input_shape=(maxlen, len(chars))))
    #model.add(keras.layers.Dense(len(chars), activation='softmax'))

    #model.compile(loss='categorical_crossentropy', optimizer=optimizer)

model = Sequential()
model.add(LSTM(700, input_shape=(X_modified.shape[1], X_modified.shape[2]), return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(700, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(700))
model.add(Dropout(0.2))
model.add(Dense(Y_modified.shape[1], activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam')

if os.path.isfile(chosen_model + "Model.h5"):
    if chosen_model == 'shakespeare':
        model.load_weights(chosen_model + "Model.h5")
    else:
        model = keras.models.load_model(chosen_model + "Model.h5")

print_callback = LambdaCallback(on_epoch_end=on_epoch_end)

if train:
    model.fit(X_modified, Y_modified,
        batch_size=50,
        epochs=100,
        callbacks=[print_callback])
else:
    fire.Fire(generator.interact_model())


