from time import sleep
from SOD import SOD_word_list
from notifypy import Notify
import random
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
if current_directory=='func':
    add=''
else:
    add='func/'

def set_new_config():
    with open(f"{add}setting/setting.txt", "w", encoding="utf-8") as fo:
        for i in settings:
            fo.write(f"{i}: {settings[i]}\n")

with open(f"{add}setting/setting.txt", "r", encoding="utf-8") as fi:
    setting=fi.readlines()
    settings={}
    for index in setting:
        option, properties=index.strip().split(": ")
        settings[option]=properties

settings['notification']='True'

with open(f'{add}pid.txt', 'w', encoding="utf-8") as f:
    f.write(str(os.getpid()))


list_=SOD_word_list()
keys=list(list_.keys())

set_new_config()

while True:
    sleep(float(settings["waiting time"])*360)
    word=random.choice([list_[key] for key in keys])
    notification = Notify(default_notification_application_name="SODA Open Dictionary", default_notification_icon=f'{add}Logo.ico', default_notification_audio=f"{add}setting/sound_effect/noti.wav")
    notification.title = f'{word["word"]} ({word["type"]})'
    notification.message = f'{word["definition"]}'
    notification.send()