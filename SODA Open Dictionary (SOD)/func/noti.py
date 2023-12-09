from time import sleep
from SOpenDict import SOD_word_list
from notifypy import Notify
import random

while True:
    sleep(10)
    word=random.choice(SOD_word_list())
    notification = Notify(default_notification_application_name="SODA Open Dictionary", default_notification_icon='func/Logo.png', default_notification_audio="func/setting/sound_effect/noti.wav")
    notification.title = f'{word["word"]} ({word["type"]})'
    notification.message = f'{word["definition"]}'
    notification.send()