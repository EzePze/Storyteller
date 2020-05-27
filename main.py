from __future__ import print_function
import sys
import os
stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')
from keras.callbacks import LambdaCallback
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.layers import RNN
from keras.utils import np_utils
import keras
sys.stderr = stderr
import numpy as np
import random
import hashlib
import generator
import re
import fire
import getpass
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

def main(
    username='',
    password='',
    model_name='',
    ):
    """
    AI Text Generation

    StoryTeller is an AI driven story generation software powered, in part, by OpenAI's gpt-2 model -- an unsupervised learning model that comes in four different versions with varying amounts of paramaters, all of which are included in this package: 
    
      - 124M
      - 355M
      - 774M
      - 1558M
      
    The names of these models represent how many parameters they have; essentially, the higher the number, the more complex the model.


    """
    class User:
        def __init__(self, username, password):
            self.username = username
            self.password = password
            self.modelList = '%sModels.txt' % self.username
            self.path = '%s/Users/%s/' % (os.getcwd(),self.username)
            #with open(self.modelList, 'w') as defaultList:
            #    defaultList.write('general\nnietzsche\nshakespeare')

        def add_new_user(self):
            with open('users.txt', 'a') as users:
                users.write('%s, %s\n' %(self.username, hashlib.sha256(str.encode(self.password)).hexdigest()))
            os.makedirs(self.path)
            with open(os.path.join(self.path + self.modelList), 'w') as defaultList:
                defaultList.write('general\nnietzsche\nshakespeare')

        def update_dict(self):
            data = read_data(os.path.join(self.path + self.modelList)).lower()
            return dict((i,c) for i,c in enumerate(data.split(), 2))

        def create_model(self, name='', data=''):
            if not name:
                name = input('\nEnter the name for your new model: ').lower()
            if not data:
                data = input('\nEnter the name of the text file to be used for modelling (needs to be in the /Storyteller folder): ')
            while not os.path.isfile(data):
                print('\nInvalid file. Are you sure the file \'%s\' is in the /Storyteller folder?\n' % data)
                data = input('\nEnter the name of the text file to be used for modelling (needs to be in the /Storyteller folder): ')
            model_dict = update_dict()
            with open(self.modelList, 'a') as modelList:
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



    def model_config_driver():
        try:
            printing('Attempting to create model named "shakespearecopy" with data "shakespeare.txt"...')
            create_model('shakespearecopy', 'shakespeare.txt')
            assert os.path.isfile('shakespearecopy.txt')
            assert read_data('shakespearecopy.txt') == read_data('shakespeare.txt')
            print('Test1 Passed.')
        except:
            print('Test1 Failed.')
        #try:
            #printing('')

    def read_data(file_name):
        #open and read text file
        text = open(file_name, encoding='utf-8').read()
        return text

    def get_model_selection():
        print("Select a model or create a new one:\n\n[0] New Model\n[1] Delete Model")
        for i in model_dict:
            print('[%d] %s' % (i, model_dict[i].title()))
        print()
        model_select = int(input())
        print()
        return model_select

    def get_login():
        return input('Welcome To StoryTeller.\n\nDo you wish to log in, or register an new user?\n\n[L]ogin\n[R]egister\n\n').upper()

    print("  _________ __                       ___________    .__  .__                ")
    print(" /   _____//  |_  ___________ ___.__.\__    ___/___ |  | |  |   ___________ ")
    print(" \_____  \    __\/  _ \_  __ \   |  |  |    |_/ __ \|  | |  | _/ __ \_  __ \ ")
    print(" /        \|  | (  (_) |  | \/\___  |  |    |\  ___/|  |_|  |_\  ___/|  | \/")
    print("/_______  /|__|  \____/|__|   /_____|  |____| \___  |____/____/\___  |__|   ")
    print("        \/                    \/                  \/               \/       ")
    print("")
    print("")
    print("")

    login = get_login()

    auth = False
    while not auth:
        while login not in 'LR':
            print('Invalid option. Choose either "L" to login or "R" to register a new user\n\n')
            login = get_login()
        if login == 'L':
            credentials = read_data("users.txt")
            rows = credentials.split("\n")
            i = 0
            username = input("Username: ").lower()
            password = getpass.getpass("Password: ").lower()

            while not auth and i < len(rows) - 1:
                compare = rows[i].split(', ')
                if username == compare[0] and hashlib.sha256(str.encode(password)).hexdigest() == compare[1]:
                    auth = True
                i += 1

            if not auth:
                print("Invalid login. Try again.\n")
                login = get_login()

            else:
                user = User(username,password)
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


    print("Login successful. Welcome, %s.\n" %user.username)

    while True:
        model_dict = user.update_dict()
        model_select = get_model_selection()

        while model_select not in range(2, len(model_dict) + 2):
            if not model_select:
                create_model(name='',data='')
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

        custom = (input('Select a mode:\n\n[C]ustom prompt\n[T]ext file prompt\n\n').upper() == "C")

        
        text = read_data(chosen_model + ".txt")
        length = len(text)
        words = text.replace('\n', ' ').split()
        start_index = random.randint(0, len(words) - 1)
        raw_text = ' '.join(words[start_index: start_index + 200])

        complex_dict = {'0':'124M', '1':'355M', '2':'774M', '3':'1558M'}

        complexity = complex_dict[input('\nChoose the level of complexity for the model:\n\n[0] Speed [----------] Quality [--        ]\n[1] Speed [-------   ] Quality [----      ]\n[2] Speed [----      ] Quality [-------   ]\n[3] Speed [--        ] Quality [----------]\n\n')]

        generator.interact_model(custom, raw_text, model_name=complexity)

if __name__ == '__main__':
    fire.Fire(main)
