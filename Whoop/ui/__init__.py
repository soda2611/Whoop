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

import eng_to_ipa, os, random, threading , pyttsx3, subprocess, signal, getpass, sys, datetime, json, shutil
from gtts import gTTS
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
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivy.uix.image import Image
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.card import MDCard
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.snackbar.snackbar import MDSnackbar
from kivymd.uix.fitimage.fitimage import FitImage
from kivymd.uix.transition.transition import MDFadeSlideTransition
from kivymd.uix.bottomsheet import *
from kivy.uix.label import Label
from kivy.uix.layout import Layout
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.clipboard import Clipboard as pyperclip
from kivy.core.audio import SoundLoader
from kivy.animation import Animation
from kivy.properties import *
from func.SOD import *
from googletrans import Translator
from functools import partial
from collections import OrderedDict

class MDCard(MDCard):
    opacity = NumericProperty(1)

    def add_widget(self, widget, *args, **kwargs):
        super().add_widget(widget, *args, **kwargs)
        widget.opacity = self.opacity
        self.bind(opacity=lambda instance, value: setattr(widget, 'opacity', value))

class MDBoxLayout(MDBoxLayout):
    opacity = NumericProperty(1)

    def add_widget(self, widget, *args, **kwargs):
        super().add_widget(widget, *args, **kwargs)
        widget.opacity = self.opacity
        self.bind(opacity=lambda instance, value: setattr(widget, 'opacity', value))

class MDLabel(MDLabel, TouchBehavior):
    def __init__(self, **kwargs):
        super(MDLabel, self).__init__(**kwargs)
        
    def on_double_tap(self, *args):
        pass
        
    def on_triple_tap(self, *args):
        if self.allow_copy:
            pyperclip.copy(self.text)
        
            MDSnackbar(MDLabel(text="Đã sao chép nội dung", theme_text_color="Custom", text_color=primarycolor), md_bg_color=menubg, y=dp(10),  size_hint_x=.85, pos_hint={"center_x": 0.5}, radius=[dp(25), dp(25), dp(25), dp(25)]).open()

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
 
class FlowLayout(Layout):
    spacing = ListProperty([0, 0])
    padding = ListProperty([0, 0, 0, 0])
    line_spacing = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super(FlowLayout, self).__init__(**kwargs)
        self.bind(size=self._trigger_layout)
        self.bind(pos=self._trigger_layout)
    
    def _trigger_layout(self, *args):
        self.do_layout()

    def do_layout(self, *args):
        width, height = self.size
        x, y = self.padding[0], height - self.padding[1]
        line_height = 0
        max_line_height = 0
        for child in reversed(self.children):
            if child.size_hint_x:
                child.width = width * child.size_hint_x
            if child.size_hint_y:
                child.height = height * child.size_hint_y

            if x + child.width > width:
                x = self.padding[0]
                y -= line_height + self.spacing[1] + self.line_spacing
                line_height = 0

            child.pos = x, y - child.height
            x += child.width + self.spacing[0]

            line_height = max(line_height, child.height)
            max_line_height = max(max_line_height, y - line_height)

        self.height = max(self.height, height - (y - self.padding[1]) + self.padding[3])

class check_button(MDIconButton):
    def __init__(self, folder, **kwargs):
        super(check_button, self).__init__(**kwargs)
        self.folder=folder
        self.icon="check"
        self.theme_icon_color="Custom"
        self.icon_color=primarycolor
        self.pos_hint={"center_x": 0.5, "center_y": 0.5}

def set_opacity_recursive(w, value=0):
        w.opacity = value

def set_y(w):
    w.y=w.y-w.parent.height*0.5

def set_x(w):
    w.x=w.x-w.parent.width*0.5
    
def fade_in_vertical(w):
    anim=Animation(opacity=1, duration=0.5)&Animation(y=w.y+w.parent.height*0.5, duration=0.75, transition='out_quad')
    anim.start(w)

def fade_out_vertical(w):
    anim=Animation(opacity=0, duration=0.5)&Animation(y=w.y-w.parent.height*0.5, duration=0.75, transition='out_quad')
    anim.start(w)

def fade_in_horizontal(w):
    anim=Animation(opacity=1, duration=0.5)&Animation(x=w.x+w.parent.width*0.5, duration=0.75, transition='out_quad')
    anim.start(w)

def fade_out_horizontal(w):
    anim=Animation(opacity=0, duration=0.5)&Animation(x=w.x-w.parent.width*0.5, duration=0.75, transition='out_quad')
    anim.start(w)
        
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
    elif settings['uid']!='none' and not os.path.exists(f"func/setting/{settings['uid']}.txt"):
        download_file("whoop_database", f"users/{settings['uid']}.txt", f"func/setting/{settings['uid']}.txt")
    try: engine = pyttsx3.init()
    except: engine = None
    data_=SOD_word_list()
    word__=[i for i in data_]
    source=word_data()
    home__=[]
    queried={}
    version=settings["version"]

    Window.minimum_width, Window.minimum_height= 500, 500 
    Window.softinput_mode='below_target'
    LabelBase.register(name="main", fn_regular=f"func/setting/fonts/{settings['fonts']}.ttf")

    color=settings["current palette"].split("; ")
    bg=[int(i)/255 for i in color[0].split(", ")]+[1]
    boxbg=[int(i)/255 for i in color[1].split(", ")]+[1]
    menubg=[int(i)/255 for i in color[2].split(", ")]+[1]
    btn=[int(i)/255 for i in color[3].split(", ")]+[1]
    primarycolor=[int(i)/255 for i in color[4].split(", ")]+[1]
    secondarycolor=[int(i)/255 for i in color[5].split(", ")]+[1]

    with open(settings["favlist"], encoding="utf-8") as fi:
        favlist=OrderedDict(eval(fi.read()))
        
    fav={}
    for i in favlist:
        for j in favlist[i]:
            fav[j]=i
    
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
    
    return bg, boxbg, menubg, btn, primarycolor, secondarycolor, colors, recent_search, fonts_name, engine, word__, source, home__, queried, version, data_, favlist, fav

def restart(instance):
    set_new_config()
    file_name = os.path.basename(__file__)
    if file_name.endswith('.py'):
        subprocess.Popen(['python', "UI.py"], start_new_session=True)
    elif file_name.endswith('.exe'):
        subprocess.Popen([file_name], start_new_session=True)
    os.kill(os.getpid(), signal.SIGTERM)
    
def remove_keys_by_value(d, value):
    keys_to_remove = [key for key, val in d.items() if val == value]
    for key in keys_to_remove:
        del d[key]
    return d

bg, boxbg, menubg, btn, primarycolor, secondarycolor, colors, recent_search, fonts_name, engine, word__, source, home__, queried, version, data_, fav_list, fav=config()
firstscreen=None
secondscreen=None
sm = MDScreenManager(transition=MDFadeSlideTransition())
