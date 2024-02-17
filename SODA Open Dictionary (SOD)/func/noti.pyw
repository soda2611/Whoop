from time import sleep
from SOD import SOD_word_list
from notifypy import Notify
import random, os, winshell, getpass

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

sod_dir = settings["title"]
icon_file = os.path.abspath(f"{sod_dir}/func/Logo.ico")
shortcut_name = settings["title"]
shortcut = os.path.join(r'C:/Users/%s/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup' %getpass.getuser() , shortcut_name + ".lnk")
current_dir = os.path.dirname(os.path.abspath(__file__))
with winshell.shortcut(shortcut) as link:
    link.path = os.path.abspath("func/run.bat")
    link.description = "run.bat"
    link.arguments = os.path.abspath("func/run.bat")
    link.icon_location = (icon_file, 0)
    link.working_directory = current_dir+r"\func"

set_new_config()

while True:
    sleep(float(settings["waiting time"])*360)
    word=random.choice([list_[key] for key in keys])
    notification = Notify(default_notification_application_name="SODA Open Dictionary", default_notification_icon=f'{add}Logo.ico', default_notification_audio=f"{add}setting/sound_effect/noti.wav")
    notification.title = f'{word["word"]} ({word["type"]})'
    notification.message = f'{word["definition"]}'
    notification.send()