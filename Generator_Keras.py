from __future__ import print_function
from keras.callbacks import LambdaCallback
import keras
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
    text = open(file_name, 'r').read()
    return text.lower()


credentials = read_data("login.txt")
rows = credentials.split("\n")
login = False

while not login:
    i = 0
    user = input("Username: ").lower()
    password = input("Password: ").lower()

    while not login and i < len(rows) - 1:

        compare = rows[i].split(', ')
        if user == compare[0] and hashlib.sha256(str.encode(password)).hexdigest() == compare[1]:
            login = True
        i += 1

    if not login:
        print("Invalid login. Try again.\n")

print("Login successful. Welcome, %s.\n" %user)

model_dict = {"1": "general", "2" : "nietzsche"}

model_select = input("""Select a model:

[1] General
[2] Nietzsche

""")

chosen_model = model_dict[model_select]

train = (input("""Select a mode:

[1]Train the model
[2]Generate text with the model

""") == "1")


text = read_data(chosen_model + ".txt")

chars = sorted(list(set(text)))
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

if train:
    print('corpus length:', len(text))
    print('total chars:', len(chars))

# cut the text in semi-redundant sequences of maxlen characters
maxlen = 40
step = 3
sentences = []
next_chars = []

for i in range(0, len(text) - maxlen, step):
    sentences.append(text[i: i + maxlen])
    next_chars.append(text[i + maxlen])

x = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        x[i, t, char_indices[char]] = 1
    y[i, char_indices[next_chars[i]]] = 1

if train:
    print('corpus length:', len(text))
    print('total chars:', len(chars))
    print('nb sequences:', len(sentences))
    print('Vectorization...')

# load the model: a single LSTM
print("loading model %s" % (chosen_model))
print("")
print("------------------------------------------------------")

if not os.path.isfile(chosen_model + "Model.h5"):
    model = keras.Sequential()
    model.add(keras.layers.LSTM(128, input_shape=(maxlen, len(chars))))
    model.add(keras.layers.Dense(len(chars), activation='softmax'))

    optimizer = keras.optimizers.RMSprop(learning_rate=0.01)
    model.compile(loss='categorical_crossentropy', optimizer=optimizer)

else:
    model = keras.models.load_model(chosen_model + "Model.h5")

def sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

def generateText():
    start_index = random.randint(0, len(text) - maxlen - 1)
    for diversity in [0.2, 0.5, 1.0, 1.2]:
        print("""
        """)
        print('----- Diversity:', diversity)
        print(""" """)

        generated = ''
        sentence = text[start_index: start_index + maxlen]
        generated += sentence
        print('----- Generating with seed: "' + sentence + '"')
        print("""
        """)
        sys.stdout.write(generated)

        for i in range(400):
            x_pred = np.zeros((1, maxlen, len(chars)))
            for t, char in enumerate(sentence):
                x_pred[0, t, char_indices[char]] = 1.

            preds = model.predict(x_pred, verbose=0)[0]
            next_index = sample(preds, diversity)
            next_char = indices_char[next_index]

            sentence = sentence[1:] + next_char

            sys.stdout.write(next_char)
            sys.stdout.flush()
        print()


def on_epoch_end(epoch, _):
    # Function invoked at end of each epoch. Prints generated text.
    # serialize model to JSON

    print("saving model")
    model.save(chosen_model + "Model.h5")

    print()
    print('----- Generating text after Epoch: %d' % epoch)

    generateText()

print_callback = LambdaCallback(on_epoch_end=on_epoch_end)

if train:
    model.fit(x, y,
        batch_size=128,
        epochs=60,
        callbacks=[print_callback])
else:
    generateText()


