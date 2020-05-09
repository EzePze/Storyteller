from __future__ import print_function
from keras.callbacks import LambdaCallback
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.layers import RNN
from keras.utils import np_utils
import numpy as np
import random
import sys
import os
import hashlib

print("  _________ __                       ___________    .__  .__                ")
print(" /   _____//  |_  ___________ ___.__.\__    ___/___ |  | |  |   ___________ ")
print(" \_____  \    __\/  _ \_  __ \   |  |  |    |_/ __ \|  | |  | _/ __ \_  __ \ ")
print(" /        \|  | (  (_) |  | \/\___  |  |    |\  ___/|  |_|  |_\  ___/|  | \/")
print("/_______  /|__|  \____/|__|   /_____|  |____| \___  |____/____/\___  |__|   ")
print("        \/                    \/                  \/               \/       ")
print("")
print("")
print("")

def read_data(file_name):
    #open and read text file
    text = open(file_name, encoding='utf-8').read()
    return text.lower()


#credentials = read_data("loginTEST.txt")
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

model_dict = {"1": "general", "2" : "nietzsche", '3' : 'shakespeare'}

model_select = input("""Select a model:

[1] General
[2] Nietzsche
[3] Shakespeare

""")

chosen_model = model_dict[model_select]

train = (input("""Select a mode:

[1]Train the model
[2]Generate text with the model

""") == "1")


text = read_data(chosen_model + "TEST.txt")

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

#if not os.path.isfile(chosen_model + "ModelTEST.h5"):
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

if os.path.isfile(chosen_model + "ModelTEST.h5"):
    if chosen_model == 'shakespeare':
        model.load_weights(chosen_model + "ModelTEST.h5")
    else:
        model = keras.models.load_model(chosen_model + "ModelTEST.h5")

# def sample(preds, temperature=1.0):
#     # helper function to sample an index from a probability array
#     preds = np.asarray(preds).astype('float64')
#     preds = np.log(preds) / temperature
#     exp_preds = np.exp(preds)
#     preds = exp_preds / np.sum(exp_preds)
#     probas = np.random.multinomial(1, preds, 1)
#     return np.argmax(probas)

def generateText():
    start_index = random.randint(0, len(text) - maxlen - 1)
    generated = ''
    sentence = text[start_index: start_index + maxlen]
    generated += sentence
    print('----- Generating with seed: "' + sentence + '"')
    print("""
    """)
    sys.stdout.write(generated)

    string_mapped = X[99]

    for i in range(400):
        x = np.reshape(string_mapped,(1,len(string_mapped), 1))
        x = x / float(len(chars))

        preds = model.predict(x, verbose=0)[0]
        next_index = np.argmax(preds)
        next_char = indices_char[next_index]

        sentence = sentence[1:] + next_char

        sys.stdout.write(next_char)
        sys.stdout.flush()
        
        string_mapped.append(next_index)
        string_mapped = string_mapped[1:len(string_mapped)]
    print()


def on_epoch_end(epoch, _):
    # Function invoked at end of each epoch. Prints generated text.

    print("saving model")
    model.save(chosen_model + "ModelTEST.h5")

    print()
    #print('----- Generating text after Epoch: %d' % epoch)

    #generateText()

print_callback = LambdaCallback(on_epoch_end=on_epoch_end)

if train:
    model.fit(x, y,
        batch_size=50,
        epochs=100,
        callbacks=[print_callback])
else:
    generateText()


