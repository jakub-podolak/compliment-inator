from gtts import gTTS
from io import BytesIO
from playsound import playsound
from time import sleep
import random
import sys
import os
import configparser

#Jakub Podolak (jjp241) 2019 Project - totally OpenSource

#get dict where each name has its own array of sayings
def get_names_text_dict(config):
    sayings_data = config.items("SAYINGS")
    sayings_dict = dict()
    for name,text in sayings_data:
        if name in sayings_dict:
            sayings_dict[name].append(text)
        else:
            sayings_dict[name] = [text]
    return sayings_dict

def run():
    #initialize config parser, read from config file passed as an argument
    config_file = sys.argv[1]
    config = configparser.ConfigParser()
    config.read(config_file)

    #get some settings from config file
    language = config['SETTINGS']['language']
    welcome_message = config['SETTINGS']['welcome_message']
    input_file = config['SETTINGS']['input_file']
    sleep_time = float(config['SETTINGS']['sleep_time'])
    start_sleep = float(config['SETTINGS']['start_sleep'])
    print_names = config['SETTINGS'].getboolean('print_names')
    output_sound = config['SETTINGS']['output_sound']

    sayings_dict = get_names_text_dict(config)

    #write something to our input file to prevent reading from empty file
    buffer = open(input_file, "a")
    buffer.write('foo')
    buffer.close()

    #variable storing size of our input file, so we run only when new face appears
    file_size = os.stat(input_file).st_size

    #say welcome message
    tts = gTTS(welcome_message, language)
    tts.save(output_sound)
    playsound(output_sound)
    sleep(start_sleep)

    while True:
        new_size = os.stat(input_file).st_size
        if file_size != new_size: #prevents from running for the same face multiple times
            file = open(input_file,'r')
            file_size = new_size
            name = file.readlines()[-1].rstrip('\n')
            if print_names:
                print(name)
            if name in sayings_dict:
                #play randomly chosen saying for our face
                tts = gTTS(sayings_dict[name][random.randint(0,len(sayings_dict[name])-1)],language)
                tts.save(output_sound)
                playsound(output_sound)
            sleep(sleep_time)

run()
