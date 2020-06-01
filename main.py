from __future__ import print_function
import download_models
import getpass
import fire
import re
import generator
import hashlib
import random
import numpy as np
import keras
from keras.utils import np_utils
from keras.layers import RNN
from keras.layers import LSTM
from keras.layers import Dropout
from keras.layers import Dense
from keras.models import Sequential
from keras.callbacks import LambdaCallback
import sys
import os
stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')
sys.stderr = stderr
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


def main():
    """
    STORYTELLER

    StoryTeller is an AI driven story generation software powered, in part, by OpenAI's gpt-2 model -- an unsupervised learning model that comes in four different versions with varying amounts of paramaters, all of which are included in this package: 

      - 124M
      - 355M
      - 774M
      - 1558M

    The names of these models represent how many parameters they have; essentially, the higher the number, the more complex the model.


    """
    # Class for every user; ensures that each user has their own model list and subsequent model_dict that gets edited, rather than a collective pool
    class User:
        # On initialisation, create a username, password, path, and modelList within that path
        def __init__(self, username, password):
            self.username = username
            self.password = password
            self.path = '%s/Users/%s/' % (os.getcwd(), self.username)
            self.modelList = self.path + '%sModels.txt' % self.username

        # If a new user, create a new directory and modelList file in the path specified above. The model list has the default models: general, nietzsche, and shakespeare. The passwords are stored in a public text file, but are hashed and encrypted.
        def add_new_user(self):
            with open('users.txt', 'a') as users:
                users.write('%s, %s\n' % (self.username, hashlib.sha256(
                    str.encode(self.password)).hexdigest()))
            os.makedirs(self.path)
            with open(os.path.join(self.modelList), 'w') as defaultList:
                defaultList.write('general\nnietzsche\nshakespeare\n')

        # If there is a change in a user's modelList, their dictionary has to be updated so the models they can select from are current and accurate
        def update_dict(self):
            data = read_data(os.path.join(self.modelList))
            return dict((i, c) for i, c in enumerate(data.split(), 2))

        # Function to create a new model -- Parameters are as follows
        #       name : The name of the model, e.g. 'Shakespeare'
        #       data : Name of the text file to be used for prompts and input, e.g. 'shakespeare.txt'
        #       test: Boolean flag to be used in the test driver, signifies that the result should be returned if successful
        def create_model(self, name='', data='', test=False):
            if not name:
                name = input('\nEnter the name for your new model: ').lower()
            if not data:
                data = input(
                    '\nEnter the name of the text file to be used for modelling (needs to be in the /Storyteller folder): ')

            # Ensures that *data* exists
            while not os.path.isfile(data):
                if test:
                    return True
                print(
                    '\nInvalid file. Are you sure the file \'%s\' is in the /Storyteller folder?\n' % data)
                data = input(
                    '\nEnter the name of the text file to be used for modelling (needs to be in the /Storyteller folder): ')

            # Ensures that the user has not already made a model with name *name*
            if name in read_data(os.path.join(self.modelList)):
                if test:
                    return True
                print('That model already exists!')
                return

            # Write the new model to the user's modelList
            with open(os.path.join(self.modelList), 'a') as modelList:
                modelList.write(name + '\n')

            # Create a new text file that contains the data to be used for prompts; named after the model
            with open('%s.txt' % name, 'w') as newData:
                newData.write(read_data(data))

            print('\nCreated model \'%s\'\n' % name)

        # Essentially the 'create_model' function in reverse, but works even if the model text file is already deleted but the model is still in the user's modelList, and vice versa
        def delete_model(self, name):
            oldList = read_data(os.path.join(self.modelList)).lower()
            oldList = oldList.replace(name, '')
            with open(os.path.join(self.modelList), 'w') as newList:
                newList.write(oldList)
            if os.path.isfile(name + ".txt"):
                os.remove('%s.txt' % name)
            print('Deleted model \'%s\'\n' % name)
            model_dict = user.update_dict()

    # Tests the 'create_model' function
    def model_config_driver(user):
        print('---------------------------\nBEGIN DRIVER\n---------------------------\n')
        print('Attempting to create model named "shakespearecopy" with data "shakespeare.txt"...')
        try:
            user.create_model('shakespearecopy', 'shakespeare.txt')
        except:
            e = sys.exc_info()[0]
            print('An error occurred: %s' % e)
        if os.path.isfile('shakespearecopy.txt') and read_data('shakespearecopy.txt') == read_data('shakespeare.txt'):
            print('Test1 Passed.')
        else:
            print('Test1 Failed.')

        print('\nAttempting to create model named "tharihtosrah" with data "lizard"')
        try:
            test = user.create_model('tharihtosrah', 'lizard', test=True)
        except:
            e = sys.exc_info()[0]
            print('An error occurred: %s' % e)
        if test:
            print('Test2 Passed.')
        else:
            print('Test2 Failed.')

        print('\nAttempting to create multiple models with the same name...\n')
        try:
            test = user.create_model(
                'shakespeare', 'shakespeare.txt', test=True)
        except:
            e = sys.exc_info()[0]
            print('\nAn error occurred: %s\n' % e)
        if test:
            print('Test3 Passed.')
        else:
            print('Test3 Failed.')

        print('\nDeleting test models...\n')
        user.delete_model('shakespearecopy')
        print('---------------------------\nEND DRIVER\n---------------------------\n')

    # reads in a text file and returns it
    def read_data(file_name):
        # open and read text file
        text = open(file_name, encoding='utf-8').read()
        return text

    # Gets the user's selection out of the options between creating a model, deleting a model, and selecting a preexisting model
    def get_model_selection():
        print(
            "Select a model or create a new one:\n\n[0] New Model\n[1] Delete Model")
        for i in model_dict:
            print('[%d] %s' % (i, model_dict[i].title()))
        print()
        model_select = int(input())
        print()
        return model_select

    # Gets whether the user wishes to login or register a new user
    def get_login():
        return input('Welcome To StoryTeller.\n\nDo you wish to log in, or register a new user?\n\n[L]ogin\n[R]egister\n\n').upper()

    print("  _________ __                       ___________    .__  .__                ")
    print(" /   _____//  |_  ___________ ___.__.\__    ___/___ |  | |  |   ___________ ")
    print(" \_____  \    __\/  _ \_  __ \   |  |  |    |_/ __ \|  | |  | _/ __ \_  __ \ ")
    print(
        " /        \|  | (  (_) |  | \/\___  |  |    |\  ___/|  |_|  |_\  ___/|  | \/")
    print("/_______  /|__|  \____/|__|   /_____|  |____| \___  |____/____/\___  |__|   ")
    print("        \/                    \/                  \/               \/       ")
    print("")
    print("")
    print("")

    # Checks if the user has the models installed; if not, install them using the 'download_models' script. This will run on the user's first usage of StoryTeller, as the models are ~ 15GB in size and so will not be packaged in the git repository
    if not os.path.isdir('models'):
        if input('It seems that you do not have the required models downloaded. These are required to generate text, and are, in total, approximately 10GB in size. Would you like to install them now? (y/n)\n\n').lower() == 'y':
            print(
                '---------------------------\nBEGIN INITIALISATION\n---------------------------\n')
            download_models.download()
            print(
                '---------------------------\nEND INITIALISATION\n---------------------------\n')
        else:
            print('\n\nExiting...')
            sys.exit()
    login = get_login()

    # Repeatedly keeps the user in a login screen until either [1] they enter a valid login, or [2] they register a new user
    auth = False
    while not auth:
        # Ensures that the user chooses either 'login' or 'register'
        while login not in 'LR':
            print(
                'Invalid option. Choose either "L" to login or "R" to register a new user\n\n')
            login = get_login()

        # Reads in the text file containing all valid usernames and hashed passwords, and performs a linear search for the credentials the user has provided
        if login == 'L':
            credentials = read_data("users.txt")
            rows = credentials.split("\n")
            i = 0
            username = input("Username: ").lower()
            password = getpass.getpass("Password: ").lower()

            # Hashes the inputted password, and compares that against the hashes in the text file. Since the hashes are computed with the same algorithm and with no random elements, the hashed password the user attempts to login with will always match the hashed password on the text file, assuming the plaintext password in both situations are the same
            while not auth and i < len(rows) - 1:
                compare = rows[i].split(', ')
                if username == compare[0] and hashlib.sha256(str.encode(password)).hexdigest() == compare[1]:
                    auth = True
                i += 1

            if not auth:
                print("Invalid login. Try again.\n")
                login = get_login()

            else:
                user = User(username, password)
        else:
            username = input('Enter a username: ')
            password = getpass.getpass('\nEnter a password: ')
            if username in read_data('users.txt'):
                print('Username "%s" already exists!' % username)
                login = get_login()
            else:
                user = User(username, password)
                user.add_new_user()
                auth = True

    print("Login successful. Welcome, %s.\n" % user.username)

    # user.create_model()
    model_config_driver(user)

    while True:
        model_dict = user.update_dict()
        model_select = get_model_selection()

        while model_select not in range(2, len(model_dict) + 2):
            if not model_select:
                user.create_model(name='', data='')
                model_dict = user.update_dict()
                model_select = get_model_selection()

            elif model_select == 1:
                print('\nWhich model do you wish to delete?\n')
                for i in model_dict:
                    print('[%d] %s' % (i - 2, model_dict[i].title()))
                print()
                name = int(input())
                if input('Are you sure you wish to delete model \'%s\'? (y/n)\n\n' % model_dict[name + 2]) == 'y':
                    print()
                    user.delete_model(model_dict[name + 2])
                    #model_dict = user.update_dict()
                    print('\nReturning to model selection screen...\n\n')
                else:
                    print('Cancelling...\n\nReturning to model selection...\n')
                model_select = get_model_selection()

            else:
                print('Please choose a number in the provided range\n')
                model_select = get_model_selection()

        chosen_model = model_dict[model_select]

        custom = (input(
            'Select a mode:\n\n[C]ustom prompt\n[T]ext file prompt\n\n').upper() == "C")

        text = read_data(chosen_model + ".txt")
        length = len(text)
        words = text.split()
        start_index = random.randint(0, len(words) - 1)
        raw_text = ' '.join(words[start_index: start_index + 200])

        complex_dict = {'0': '124M', '1': '355M', '2': '774M', '3': '1558M'}

        complexity = complex_dict[input(
            '\nChoose the level of complexity for the model:\n\n[0] Speed [----------] Quality [--        ]\n[1] Speed [-------   ] Quality [----      ]\n[2] Speed [----      ] Quality [-------   ]\n[3] Speed [--        ] Quality [----------]\n\n')]

        generator.interact_model(custom, raw_text, model_name=complexity)


if __name__ == '__main__':
    try:
        fire.Fire(main)
    except KeyboardInterrupt:
        print('\n' + '=' * 80 + '\n\nQUITTING\n\n' + '=' * 80 + '\n')
