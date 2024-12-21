from func.necessary_function import get_config, check_connection
from func.data_manager import *
from kivy.config import Config

settings=get_config()

try:
    width, height= settings["size"].split()

    Config.set('graphics', 'width', str(width))
    Config.set('graphics', 'height', str(height))
except:
    pass

import eng_to_ipa, os, random, threading , pyttsx3, subprocess, signal, getpass, sys, datetime, json
from kivymd.app import MDApp
from kivymd.uix.behaviors.magic_behavior import MagicBehavior
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton, MDFillRoundFlatButton, MDFillRoundFlatIconButton
from kivy.core.text import LabelBase
from kivymd.font_definitions import theme_font_styles
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.card import MDCard
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.progressbar import MDProgressBar
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.clipboard import Clipboard as pyperclip
from func.SOD import *
from googletrans import Translator

class MDIconButton(MagicBehavior, MDIconButton):
    def __init__(self, **kwargs):
        super(MDIconButton, self).__init__(**kwargs)
        
    def on_release(self, *args):
        self.grow()
        
class MDFillRoundFlatButton(MagicBehavior, MDFillRoundFlatButton):
    def __init__(self, **kwargs):
        super(MDFillRoundFlatButton, self).__init__(**kwargs)
        
    def on_release(self, *args):
        self.grow()
        
class MDFillRoundFlatIconButton(MagicBehavior, MDFillRoundFlatIconButton):
    def __init__(self, **kwargs):
        super(MDFillRoundFlatIconButton, self).__init__(**kwargs)
        
    def on_release(self, *args):
        self.grow()

def set_new_config():
    with open("func/setting/setting.txt", "w", encoding="utf-8") as fo:
        for i in settings:
            fo.write(f"{i}: {str(settings[i])}\n")

def track_user_queries(data):
    download_file("whoop_database", f"users/{settings['uid']}.txt", f"func/data/temp_{settings['uid']}.txt")
    with open(f"func/data/temp_{settings['uid']}.txt", encoding="utf-8") as fo:
        _out_=eval(fo.read())
        _out_.update(data)
    with open(f"func/data/temp_{settings['uid']}.txt", "w", encoding="utf-8") as fo:
        fo.write(json.dumps(_out_, ensure_ascii=False, indent=4))
    upload_file("whoop_database", f"users/{settings['uid']}.txt", f"func/data/temp_{settings['uid']}.txt")
    os.remove(f"func/data/temp_{settings['uid']}.txt")

def config():
    if settings['uid']=="none":
        settings['uid']=datetime.datetime.now().strftime(f"%Y%m%d%H%M%S")
        with open(f"func/setting/{settings['uid']}.txt", "w", encoding="utf-8") as fo: fo.write("{}")
        upload_file("whoop_database", f"users/{settings['uid']}.txt", f"func/setting/{settings['uid']}.txt")
        set_new_config()
    engine = pyttsx3.init()
    data_=SOD_word_list()
    word__=[i for i in data_]
    source=word_data()
    home__=[]
    queried={}
    version=settings["version"]

    Window.minimum_width, Window.minimum_height= 406, 374
    Window.softinput_mode='pan'
    LabelBase.register(name="main", fn_regular=f"func/setting/fonts/{settings['fonts']}.ttf")

    color=settings["current palette"].split("; ")
    bg=[int(i)/255 for i in color[0].split(", ")]+[1]
    boxbg=[int(i)/255 for i in color[1].split(", ")]+[1]
    menubg=[int(i)/255 for i in color[2].split(", ")]+[1]
    btn=[int(i)/255 for i in color[3].split(", ")]+[1]
    primarycolor=[int(i)/255 for i in color[4].split(", ")]+[1]
    secondarycolor=[int(i)/255 for i in color[5].split(", ")]+[1]
    
    with open("func/setting/colors.txt", "r", encoding="utf-8") as fi:
        lines=fi.readlines()
    
    colors=[]
    for i in lines:
        colors.append([k.split(", ") for k in i.strip().split("; ")])

    with open(f"func/setting/{settings['uid']}.txt", "r", encoding="utf-8") as f:
        lines = f.read()
        recent_search = eval(lines)

    font_dir = "func/setting/fonts"
    fonts_name=[]
    for root, dirs, files in os.walk(font_dir):
        for file in files:
            if file.endswith(".ttf"):
                fonts_name.append(file[:file.find(".ttf")])
    
    return bg, boxbg, menubg, btn, primarycolor, secondarycolor, colors, recent_search, fonts_name, engine, word__, source, home__, queried, version, data_

def restart(instance):
    set_new_config()
    subprocess.Popen(["py", "UI.py"], start_new_session=True)
    os.kill(os.getpid(), signal.SIGTERM)

bg, boxbg, menubg, btn, primarycolor, secondarycolor, colors, recent_search, fonts_name, engine, word__, source, home__, queried, version, data_=config()
firstscreen=None
secondscreen=None
sm = ScreenManager()
admin_code="nah bro"
