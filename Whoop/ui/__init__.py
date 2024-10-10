from func.necessary_function import get_config, get_scaling_factor, check_connection
from func.data_manager import *
from kivy.config import Config

if check_connection(): download_file("Whoop/func/data/tu_dien_nguon.txt", "func/data/tu_dien_nguon.txt")

settings=get_config()

try:
    width, height= settings["size"].split()

    Config.set('graphics', 'width', str(width))
    Config.set('graphics', 'height', str(height))
except:
    pass

import eng_to_ipa, os, random, threading , pyttsx3, subprocess, signal, winshell, getpass, sys, psutil
from kivymd.app import MDApp
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
from kivy.clock import Clock
from kivy.core.window import Window
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

    os.remove("func/main_pid.txt")

def config():
    engine = pyttsx3.init()
    data_=SOD_word_list()
    word__=[i for i in data_]
    source=word_data()
    home__={}
    queried={}
    version=settings["version"]

    Window.minimum_width, Window.minimum_height= 406, 374
    Window.softinput_mode='pan'
    LabelBase.register(name="main", fn_regular=f"func/setting/fonts/{settings['fonts']}.ttf")

    if settings["boost performance"]=="True": settings["boost performance"]=True
    else: settings["boost performance"]=False

    color=settings["current palette"].split("; ")
    bg=[int(i)/255 for i in color[0].split(", ")]+[1]
    boxbg=[int(i)/255 for i in color[1].split(", ")]+[1]
    menubg=[int(i)/255 for i in color[2].split(", ")]+[1]
    btn=[int(i)/255 for i in color[3].split(", ")]+[1]
    primarycolor=[int(i)/255 for i in color[4].split(", ")]+[1]
    secondarycolor=[int(i)/255 for i in color[5].split(", ")]+[1]
    
    if settings["theme"]=="Light":
        with open("func/setting/light_colors.txt", "r", encoding="utf-8") as fi:
            lines=fi.readlines()
    else:
        with open("func/setting/dark_colors.txt", "r", encoding="utf-8") as fi:
            lines=fi.readlines()

    colors=[]
    for i in lines:
        colors.append([k.split(", ") for k in i.strip().split("; ")])

    with open("func/data/recent.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    recent_search = [line.replace("\n","") for line in lines]

    font_dir = "func/setting/fonts"
    fonts_name=[]
    for root, dirs, files in os.walk(font_dir):
        for file in files:
            if file.endswith(".ttf"):
                fonts_name.append(file[:file.find(".ttf")])
    
    return bg, boxbg, menubg, btn, primarycolor, secondarycolor, colors, recent_search, fonts_name, engine, word__, source, home__, queried, version, data_

bg, boxbg, menubg, btn, primarycolor, secondarycolor, colors, recent_search, fonts_name, engine, word__, source, home__, queried, version, data_=config()
firstscreen=None
secondscreen=None
scale=get_scaling_factor()
sm = ScreenManager()
admin_code="nah bro"
