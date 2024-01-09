from func.necessary_function import get_config
from kivy.config import Config

settings=get_config()

try:
    width, height= settings["size"].split()

    Config.set('graphics', 'width', str(width))
    Config.set('graphics', 'height', str(height))
except:
    pass

import eng_to_ipa
import os
import random
import threading 
import pyttsx3
import subprocess
import signal
import winshell
import getpass
from notifypy import Notify
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton, MDFillRoundFlatButton, MDFillRoundFlatIconButton
from kivy.core.text import LabelBase
from kivymd.font_definitions import theme_font_styles
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.card import MDCard
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.progressbar import MDProgressBar
from kivy.clock import Clock
from kivy.core.window import Window
from func.SOD import SOD,grammar_structure_detector,SOD_word_list,word_detector, data, word_data
from googletrans import Translator

engine = pyttsx3.init()
version="1.0.0dev"
data_=data()
source=word_data()

Window.minimum_width, Window.minimum_height= 406, 374
Window.softinput_mode='pan'
translator = Translator()
LabelBase.register(name="main", fn_regular=f"func/setting/fonts/{settings['fonts']}.ttf")

def set_new_config():
    with open("func/setting/setting.txt", "w", encoding="utf-8") as fo:
        for i in settings:
            fo.write(f"{i}: {settings[i]}\n")

def config():
    global boost_performance_require, bg, boxbg, menubg, btn, primarycolor, secondarycolor, colors, recent_search, fonts_name, noti_require

    if settings["boost performance"]=="True": boost_performance_require=True
    else: boost_performance_require=False

    if settings["notification"]=="True": noti_require=True
    else: noti_require=False

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

    with open("func/setting/recent.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    recent_search = []
    for line in lines:
        word, wordtype, definition, translation = line.strip().split(": ")
        recent_search.append({"word": word, "type": wordtype, "definition": definition, "translation": translation})

    font_dir = "func/setting/fonts"
    fonts_name=[]
    for root, dirs, files in os.walk(font_dir):
        for file in files:
            if file.endswith(".ttf"):
                fonts_name.append(file[:file.find(".ttf")])

class SettingLayout(MDBoxLayout):
    def __init__(self, **kwargs):
        super(SettingLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [10, 10, 10, 10]
        self.spacing = 20
        self.md_bg_color=bg
        Window.bind(on_resize=self.on_window_resize)

        self.search_thread=None
        self.icon=MDIconButton(icon="check-circle", theme_icon_color="Custom", icon_color=primarycolor, size_hint=(None, None), pos_hint={"center_x": 0.5})
        self.got_check=None
        self.got_font_check=None
        self.touch_count=0
        self.timer = None
        
        self.back_button=MDIconButton(icon="arrow-left", size_hint=(None, None), pos_hint={"left": 0})
        self.add_widget(self.back_button)
        self.back_button.bind(on_press=self.back)

        self.scrollview=ScrollView(size_hint=(1,1), do_scroll_x=False)
        self.add_widget(self.scrollview)

        self.personalize=MDBoxLayout(orientation="vertical", size_hint=(1,None), pos_hint={"center_x": 0.5}, spacing=20)
        self.personalize.bind(minimum_height=self.personalize.setter('height'))
        self.scrollview.add_widget(self.personalize)

        self.noti_box=MDBoxLayout(size_hint=(1, None), height=50, pos_hint={'center_x': 0.5, 'center_y': 0.5}, spacing = 20)
        self.noti_box.switch_box=MDBoxLayout(size_hint=(0.25, None), height=50, pos_hint={'center_x': 0.5, 'center_y': 0.5}, spacing = 20)
        self.noti_box.time_value_box=MDBoxLayout(size_hint=(0.75, None), height=50, pos_hint={'left': 0.9, 'center_y': 0.8}, spacing = 20)
        self.noti_check_title=MDLabel(text="Gợi ý từ mới qua thông báo", font_style="H6", size_hint=(1, None), height=30, pos_hint={'center_x': 0.5, 'center_y': 0.5}, theme_text_color="Custom", text_color=primarycolor)
        self.noti_check=MDSwitch(icon_inactive="close", icon_active="check", thumb_color_inactive=boxbg, thumb_color_active=boxbg, track_color_inactive=(155/255, 155/255, 155/255, 1), track_color_active=btn)
        self.noti_check.active=noti_require
        self.noti_check.bind(active=self.noti)
        self.noti_time_title=MDLabel(text="Thời gian chờ thông báo", font_style="Body2", halign="right", size_hint=(0.5, None), pos_hint={"right": 0.7}, height=30, theme_text_color="Custom", text_color=primarycolor)        
        self.noti_time=MDTextField(icon_left="clock", icon_left_color_focus=btn, text=settings["waiting time"], line_color_normal=(115, 115, 115, 1), line_color_focus=(0, 0, 0, 1), hint_text_color=(115, 115, 115, 1), hint_text_color_focus=(0, 0, 0, 1), text_color_focus=(0, 0, 0, 1), fill_color_normal=(1, 1, 1, 1), mode="round", size_hint=(None, None), pos_hint={"right": 0.75}, width=100, height=30, multiline=False, disabled=not noti_require)
        self.noti_time.bind(text=self.set_noti_time)
        self.personalize.add_widget(self.noti_check_title)
        self.personalize.add_widget(self.noti_box)
        self.noti_box.add_widget(self.noti_box.switch_box)
        self.noti_box.switch_box.add_widget(self.noti_check)
        self.noti_box.add_widget(self.noti_box.time_value_box)
        self.noti_box.time_value_box.add_widget(self.noti_time_title)
        self.noti_box.time_value_box.add_widget(self.noti_time)

        self.internet_required_check_title=MDLabel(text="Chế độ Tối ưu hiệu suất", font_style="H6", size_hint=(1, None), height=30, pos_hint={'center_x': 0.5, 'center_y': 0.5}, theme_text_color="Custom", text_color=primarycolor)
        self.internet_required_check=MDSwitch(icon_inactive="close", icon_active="check", thumb_color_inactive=boxbg, thumb_color_active=boxbg, track_color_inactive=(155/255, 155/255, 155/255, 1), track_color_active=btn)
        self.internet_required_check.active=boost_performance_require 
        self.internet_required_check.bind(active=self.boost_performance)
        self.personalize.add_widget(self.internet_required_check_title)
        self.personalize.add_widget(self.internet_required_check)

        self.changelayout=MDLabel(text="Thay đổi bố cục trang chủ", font_style="H6", halign="left", size_hint=(1,None), height=30, pos_hint={"center_x":0.5}, theme_text_color="Custom", text_color=primarycolor)
        self.layout_list=MDBoxLayout(size_hint=(None, 1), pos_hint={"center_x": 0.5}, spacing=20, padding=[10,10,10,10])
        self.layout_list.bind(minimum_width=self.layout_list.setter('width'))
        self.layout_scroll=ScrollView(do_scroll_y=False, size_hint=(1, None), height=125)
        self.layout_scroll.add_widget(self.layout_list)
        self.layout_list.add_widget(self.create_layout_preview("box"))
        self.layout_list.add_widget(self.create_layout_preview("flashcard"))

        self.changecolor=MDLabel(text="Cá nhân hóa với bảng màu", font_style="H6", halign="left", size_hint=(1,None), height=30, pos_hint={"center_x":0.5}, theme_text_color="Custom", text_color=primarycolor)
        self.color_palette_list=MDBoxLayout(size_hint=(None, 1), pos_hint={"center_x": 0.5}, spacing=20, padding=[10,10,10,10])
        self.color_palette_list.bind(minimum_width=self.color_palette_list.setter('width'))
        self.color_palette_scroll=ScrollView(do_scroll_y=False, size_hint=(1, None), height=300)
        self.color_palette_scroll.add_widget(self.color_palette_list)
        self.change_fonts=MDLabel(text="Fonts", font_style="H6", halign="left", size_hint=(1,None), height=30, pos_hint={"center_x":0.5}, theme_text_color="Custom", text_color=primarycolor)
        self.font_list=MDBoxLayout(size_hint=(None, 1), pos_hint={"center_x": 0.5}, spacing=20, padding=[10,10,10,10])
        self.font_list.bind(minimum_width=self.font_list.setter('width'))
        self.font_scroll=ScrollView(do_scroll_y=False, size_hint=(1, None), height=50)
        if (Window.width == Window.minimum_width) and (Window.height == Window.minimum_height):
            self.color_palette_scroll.pos_hint={"center_x": 0.5}
            self.font_scroll.pos_hint={"center_x": 0.5}
        else:
            self.color_palette_scroll.pos_hint={"x": 0}
            self.font_scroll.pos_hint={"x": 0}
        self.font_scroll.add_widget(self.font_list)
        self.personalize.add_widget(self.changelayout)
        self.personalize.add_widget(self.layout_scroll)
        self.personalize.add_widget(self.changecolor)
        self.personalize.add_widget(self.color_palette_scroll)
        self.personalize.add_widget(self.change_fonts)
        self.personalize.add_widget(self.font_scroll)
        for i in colors:
            self.color_palette_list.add_widget(self.create_palette(i))

        for i in fonts_name:
            self.font_list.add_widget(self.create_preview(i))

        '''self.notification=MDLabel(text="Bạn không thể thay đổi bất cứ cài đặt nào của ứng dụng trong phiên bản này. Vui lòng chờ phiên bản cập nhật tiếp theo.", font_style="H6", halign="center", size_hint=(0.75,1), pos_hint={"center_x": 0.5})
        self.add_widget(self.notification)'''
        
        self.color_palette_scroll.scroll_to(self.got_check)
        self.font_scroll.scroll_to(self.got_font_check)

        self.info=MDFillRoundFlatButton(text=f"Phiên bản: SOD {version}\nNgày phát hành: Unknown", font_style="Caption", halign="center", size_hint=(0.75,None), height=35, pos_hint={"center_x": 0.5}, theme_text_color="Custom", text_color=primarycolor, md_bg_color=bg)
        self.info.bind(on_release=self.on_touch)
        self.add_widget(self.info)

        self.dialog = MDDialog(
            title="Cài đặt liên quan đến cá nhân hóa sẽ được áp dụng khi bạn khởi động lại ứng dụng",
            type="alert",
            buttons=[
                MDFillRoundFlatButton(
                    text="Đóng",
                    md_bg_color=btn,
                    theme_text_color="Custom",
                    text_color=secondarycolor
                )
            ],
            md_bg_color=boxbg
        )
        self.dialog.buttons[0].bind(on_release=self.dialog.dismiss)

    def run_noti(self, instance):
        if os.path.exists('func/pid.txt'):
            with open('func/pid.txt', 'r') as f:
                pid = int(f.read())
                os.kill(pid, signal.SIGTERM)
            try:
                os.remove('func/pid.txt')
            except:
                pass
        settings["waiting time"]=self.noti_time.text
        with open("func/setting/setting.txt", "w", encoding="utf-8") as fo:
            for i in settings:
                fo.write(f"{i}: {settings[i]}\n")
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, "func/noti.pyw")
        self.process = subprocess.Popen(["pythonw", file_path], start_new_session=True, shell=True)
    
    def create_layout_preview(self, i):
        self.temp_box=MDCard(md_bg_color=(1,1,1,1), size_hint=(None, None), width=100, height=100, padding=[10, 10, 10, 10], spacing=20, ripple_behavior=True, on_press=lambda instance: self.change_homepage_layout(instance, "box"))
        if i=="box":
            self.temp_box.orientation="vertical"
        for i in range(2):
            box=MDCard(width=75, height=22.5, pos_hint={'center_x': 0.5}, md_bg_color=boxbg, ripple_behavior=True)
            if i=="flashcard":
                box.orientation="vertical"
            box.bind(on_press=lambda instance: self.change_homepage_layout(instance, i))
            self.temp_box.add_widget(box)
        self.temp_box.bind(on_press=lambda instance: self.change_homepage_layout(instance, i))
        
        return self.temp_box

    def change_homepage_layout(self, instance, style):
        settings["homepage style"]=style
        set_new_config()
        self.dialog.open()

    def set_noti_time(self, instance, time):
        if self.search_thread:
            self.search_thread.cancel()
        self.search_thread = threading.Timer(0.5, self.run_noti, args=(instance,))
        self.search_thread.start()

    def noti(self, instance, value):
        global noti_require
        noti_require= not noti_require
        settings["notification"]=str(noti_require)
        sod_dir = "SODA Open Dictionary (SOD)"
        icon_file = os.path.abspath(f"{sod_dir}/func/Logo.ico")
        shortcut_name = "SODA Open Dictionary"
        shortcut = os.path.join(r'C:/Users/%s/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup' %getpass.getuser() , shortcut_name + ".lnk")
        if noti_require: 
            self.noti_time.disabled=False
            settings["waiting time"]=self.noti_time.text
            with open("func/setting/setting.txt", "w", encoding="utf-8") as fo:
                for i in settings:
                    fo.write(f"{i}: {settings[i]}\n")
            status='bật'
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_dir, "func/noti.pyw")
            self.process = subprocess.Popen(["pythonw", file_path], start_new_session=True, shell=True)
            with winshell.shortcut(shortcut) as link:
                link.path = os.path.abspath("func/run.bat")
                link.description = "run.bat"
                link.arguments = os.path.abspath("func/run.bat")
                link.icon_location = (icon_file, 0)
                link.working_directory = current_dir+r"\func"
        else:
            self.noti_time.disabled=True
            status='tắt'
            if os.path.exists('func/pid.txt'):
                with open('func/pid.txt', 'r') as f:
                    pid = int(f.read())
                    os.kill(pid, signal.SIGTERM)
                try:
                    os.remove('func/pid.txt')
                except:
                    pass
            os.remove(shortcut)
        notification = Notify(default_notification_message="Chế độ này sẽ gợi ý từ mới qua thông báo mỗi ngày để giúp bạn học từ tốt hơn",
                              default_notification_application_name="SODA Open Dictionary",
                              default_notification_icon='func/Logo.ico',
                              default_notification_audio='func/setting/sound_effect/noti.wav')
        notification.title = f"Gợi ý từ qua thông báo đã {status}"
        notification.send()
        
    def create_palette(self, i):
        self.color=MDCard(md_bg_color=(1,1,1,1), orientation="vertical", size_hint=(None, None), width=50, height=200, pos_hint={"center_x": 0.5}, padding=[10, 10, 10, 10], ripple_behavior=True)
        theme=[]
        for j in i:
            theme.append([int(j[0])/255,int(j[1])/255,int(j[2])/255, 1])
        for j in i[:4]:
            self.color1=MDBoxLayout(md_bg_color=(int(j[0])/255,int(j[1])/255,int(j[2])/255, 1),size_hint=(1,0.25), pos_hint={"center_x":0.5})
            self.color.add_widget(self.color1)
        if [[str(int(i*255)) for i in bg[:-1]], [str(int(i*255)) for i in boxbg[:-1]], [str(int(i*255)) for i in menubg[:-1]], [str(int(i*255)) for i in btn[:-1]]]==i[:4]:
            self.color.height=250
            self.color.add_widget(self.icon)
            self.got_check=self.color
        self.color.bind(on_press=lambda instance: self.change_color_theme(instance, theme[0], theme[1], theme[2], theme[3], theme[4], theme[5]))

        return self.color

    def change_color_theme(self, instance, new_bg, new_boxbg, new_menubg, new_btn, new_primarycolor, new_secondarycolor):
        self.got_check.remove_widget(self.icon)
        self.got_check.height=200
        self.got_check=instance
        instance.height=250
        instance.add_widget(self.icon)
        self.color_palette_scroll.scroll_to(self.got_check)
        settings["current palette"]="; ".join([", ".join([str(int(i*255)) for i in new_bg][:-1]),", ".join([str(int(i*255)) for i in new_boxbg][:-1]),", ".join([str(int(i*255)) for i in new_menubg][:-1]),", ".join([str(int(i*255)) for i in new_btn][:-1]), ", ".join([str(int(i*255)) for i in new_primarycolor][:-1]), ", ".join([str(int(i*255)) for i in new_secondarycolor][:-1])])
        set_new_config()
        self.dialog.open()

    def create_preview(self, i):
        self.font=MDFillRoundFlatIconButton(text=i, theme_icon_color='Custom', md_bg_color=btn, theme_text_color="Custom", text_color=secondarycolor, font_name=f"func/setting/fonts/{i}.ttf", font_size=17)
        if i==settings["fonts"]:
            self.font.icon='check-circle'
            self.font.icon_color=secondarycolor
            self.got_font_check=self.font
        self.font.bind(on_press=lambda instance: self.change_font(instance, i))

        return self.font
    
    def change_font(self, instance, i):
        self.got_font_check.icon=''
        self.got_font_check=instance
        instance.icon='check-circle'
        self.font_scroll.scroll_to(self.got_font_check)
        settings["fonts"]=i
        set_new_config()
        self.dialog.open()

    def boost_performance(self, instance, value):
        global boost_performance_require
        boost_performance_require=not boost_performance_require
        settings["boost performance"]=str(boost_performance_require)

    def back(self, instance):
        sm.transition.direction = "right"
        sm.current = 'first'

    def on_touch(self, instance):
        self.cre=MDLabel(text="""Chào mừng bạn đến với SODA Open Dictionary!

Là nhà phát triển chính của SODA Open Dictionary, tôi muốn dành một chút thời gian để cảm ơn bạn đã sử dụng phần mềm của tôi.

SODA Open Dictionary được xây dựng bằng ngôn ngữ lập trình Python và sử dụng thư viện giao diện KivyMD. Tôi đã dành rất nhiều thời gian và công sức để tạo ra một sản phẩm mà tôi hy vọng sẽ hữu ích cho bạn.

Tôi rất biết ơn sự hỗ trợ và phản hồi của bạn. Những ý kiến đóng góp của bạn giúp tôi cải thiện SODA Open Dictionary và đảm bảo rằng nó đáp ứng nhu cầu của người dùng.

Nếu bạn có bất kỳ câu hỏi hoặc yêu cầu nào, đừng ngần ngại liên hệ với tôi qua email. Tôi luôn sẵn lòng giúp đỡ và mong muốn nghe ý kiến từ bạn.

Cảm ơn bạn đã sử dụng SODA Open Dictionary!

Trân trọng,
Nhật
                """,
                  font_style="Body2",
                  size_hint=(1,None),
                  height=25,
                  pos_hint={"center_x": 0.5},
                  theme_text_color="Custom",
                  text_color=primarycolor)
        self.cre.bind(texture_size=self.cre.setter('text_size'))
        self.cre.bind(texture_size=self.cre.setter('size'))
        self.temp_scroll_box=ScrollView(size_hint=(1, 1), pos_hint={"center_x": 0.5}, do_scroll_x=False)
        self.temp_scroll_box.add_widget(self.cre)
        self.container=MDCard(orientation="vertical", spacing=20, size_hint=(1,None), height=200, padding=[10,10,10,10])
        self.container.add_widget(self.temp_scroll_box)
        if self.timer is not None:
            self.timer.cancel()
        self.touch_count += 1
        if self.touch_count == 10:  # Số lần chạm xác định
            self.credit=MDDialog(
            title="Thư Cảm ơn từ Nhà phát triển SODA Open Dictionary",
            type="custom",
            content_cls=self.container,
            buttons=[
                MDFillRoundFlatButton(
                    text="Đóng",
                    md_bg_color=btn,
                    theme_text_color="Custom",
                    text_color=secondarycolor
                )
            ],
            md_bg_color=boxbg
            )
            self.credit.buttons[0].bind(on_release=self.credit.dismiss)
            self.credit.open()

            self.touch_count = 0
        else:
            self.timer = Clock.schedule_once(self.reset_touch_count, 0.5)  # Đặt lại sau 1 giây

    def reset_touch_count(self, dt):
        self.touch_count = 0

    def on_window_resize(self, window, width, height):
        if (width == Window.minimum_width) and (height == Window.minimum_height):
            self.color_palette_scroll.pos_hint={"center_x": 0.5}
        else:
            self.color_palette_scroll.pos_hint={"x": 0}

class MyLayout(MDBoxLayout, TouchBehavior):
    def __init__(self, **kwargs):
        super(MyLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [10, 10, 10, 10]
        self.spacing = 20
        Window.bind(on_resize=self.on_window_resize)

        self.md_bg_color=bg
        self.text=""
        self.signal=False
        self.search_thread = None

        theme_font_styles.append('main')
        self.theme_cls.font_styles["main"] = ["main", 16, False, 0.15]

        self.temp_box=MDBoxLayout(orientation="vertical",size_hint_y=None, padding=[10,10,10,10], spacing=20, pos_hint={"center_x": 0.5})
        self.temp_box.bind(minimum_height=self.temp_box.setter('height'))
        for i in recent_search:
            self.temp_box.add_widget(self.create_content_box(i))

        self.label = MDLabel(text='SODA Open Dictionary', font_style="H6", halign='center', valign='top', size_hint=(0.9, 0.02), pos_hint={'center_x': 0.5, 'center_y': 0.5}, height=30, theme_text_color="Custom", text_color=primarycolor)
        
        self.cautionlabel = MDLabel(text="(Kết quả có thể sai do bộ dữ liệu chưa qua kiểm tra sàng lọc)", font_style="Caption", halign='center', size_hint=(0.75, None), pos_hint={'center_x': 0.5, 'center_y': 0.5}, height=30, theme_text_color="Custom", text_color=primarycolor)

        self.resultlabel = MDLabel(text='', font_style="H6", halign='center', valign='middle', size_hint=(1, None), pos_hint={'center_x': 0.5, 'center_y': 0.5}, height=30)

        self.caplabel = MDLabel(text="Không nhập cả câu vì đây không phải là trình dịch như Google Translate", font_style="Caption", halign="center", size_hint=(0.75, None), pos_hint={'center_x': 0.5, 'center_y': 0.5}, height=30, theme_text_color="Custom", text_color=primarycolor)
        
        self.text_input = MDTextField(hint_text="Nhập từ cần tìm", line_color_normal=(115, 115, 115, 1), line_color_focus=(0, 0, 0, 1), hint_text_color=(115, 115, 115, 1), hint_text_color_focus=(0, 0, 0, 1), text_color_focus=(0, 0, 0, 1), fill_color_normal=(1, 1, 1, 1), mode="round", size_hint=(0.75, None), pos_hint={'center_x': 0.5}, height=30, multiline=False)
        
        self.button = MDIconButton(icon='magnify', theme_icon_color="Custom", icon_color=secondarycolor, size_hint=(1, None), pos_hint={"center_x":0.5})
        
        self.homebutton = MDIconButton(icon='home', theme_icon_color="Custom", icon_color=secondarycolor, size_hint=(1, None), pos_hint={"x":0})
        
        self.menubutton = MDIconButton(icon='menu', theme_icon_color="Custom", icon_color=secondarycolor, size_hint=(1, None), pos_hint={"x":1})
        
        self.progress_box=MDBoxLayout(orientation='vertical', size_hint=(0.95,None), height=5, pos_hint={"center_x":0.5})

        self.progress_bar = MDProgressBar(radius=[5,5,5,5], type="indeterminate", pos_hint={"center_x":0.5}, running_duration=0.75, catching_duration=0.5, color=btn, back_color=bg)
        self.progress_box.add_widget(self.progress_bar)

        self.add_widget(self.label)
        self.add_widget(self.cautionlabel)

        self.one_box=MDBoxLayout(size_hint=(0.85, 0.25), pos_hint={'center_x': 0.5, 'center_y': 0.5}, spacing = 20)
        self.add_widget(self.one_box)

        self.noname=MDCard(orientation='vertical',md_bg_color=bg, size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.one_box.add_widget(self.noname)

        self.recent=MDCard(orientation='vertical',md_bg_color=boxbg, size_hint=(None, 1), width=250, pos_hint={'center_x': 0.5, 'center_y': 0.5}, padding=[10,10,10,10], spacing=20)
        self.recent_label=MDLabel(text="Gần đây", font_style="H6", halign="center", size_hint=(1,None), height=25, pos_hint={"center_x": 0.5}, theme_text_color="Custom", text_color=primarycolor)
        self.recent_scrollview = ScrollView(size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5}, do_scroll_x=False)
        self.action_box=MDBoxLayout(size_hint=(1, None), height=20, spacing=20, pos_hint={"center_x":0.5})
        self.clear_action=MDFillRoundFlatButton(text="Clear", md_bg_color=btn, pos_hint={"center_x": 0.5}, theme_text_color="Custom", text_color=secondarycolor)
        self.recent_scrollview_box=MDBoxLayout(orientation='vertical', size_hint=(1, None), spacing=20)
        self.recent_scrollview_box.bind(minimum_height=self.recent_scrollview_box.setter('height'))
        self.recent.add_widget(self.recent_label)
        self.recent.add_widget(self.recent_scrollview)
        self.recent.add_widget(self.clear_action)
        self.recent_scrollview.add_widget(self.recent_scrollview_box)
        for i in recent_search:
            self.recent_scrollview_box.add_widget(self.create_content_box(i))
        self.clear_action.bind(on_release=self.clear_history)

        self.noname.add_widget(self.progress_box)

        self.scrollview = ScrollView(size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        self.result_box=MDBoxLayout(orientation='vertical', size_hint=(1,None), spacing=20, padding=[10,10,10,10])
        self.result_box.bind(minimum_height=self.result_box.setter('height'))

        self.homebox=MDBoxLayout(spacing=20)
        if settings["homepage style"]=="box":
            self.scrollview.do_scroll_x=False
            self.homebox.orientation="vertical"
            self.homebox.size_hint_y=None
            self.homebox.bind(minimum_height=self.homebox.setter('height'))
        elif settings["homepage style"]=="flashcard":
            self.scrollview.do_scroll_y=False
            self.homebox.size_hint_x=None
            self.homebox.bind(minimum_width=self.homebox.setter('width'))
        for i in range(10):
            self.homebox.add_widget(self.create_content_box(random.choice(SOD_word_list())))
        
        self.noname.add_widget(self.scrollview)
        self.scrollview.add_widget(self.homebox)
        self.refreshbutton=MDFillRoundFlatButton(text="Làm mới",size_hint=(None, None), pos_hint={"center_x":0.5, "center_y":0.5}, md_bg_color=btn, theme_text_color="Custom", text_color=secondarycolor)
        self.refreshbutton.bind(on_press=lambda instance: self.refresh(instance, None))
        self.homebox.add_widget(self.refreshbutton)
        
        self.resultlabel.bind(texture_size=self.resultlabel.setter('text_size'))
        self.resultlabel.bind(texture_size=self.resultlabel.setter('size'))
        self.resultlabel.bind(text=self.update_resultlabel)

        self.box = MDBoxLayout(size_hint=(0.9, 0.02), pos_hint={"center_x":0.5})
        self.add_widget(self.box)
        self.box.add_widget(self.text_input)

        self.taskbar=MDCard(md_bg_color=btn, radius=[25,25,25,25], size_hint=(1, None), height=50, pos_hint={"center_x":0.5, "center_y": 0.25})
        self.box.add_widget(self.taskbar)

        self.text_input.bind(focus=self.hide_input)
        self.text_input.bind(on_text_validate=self.search_button_pressed)
        self.hide_input(1,False)
        self.add_widget(self.caplabel)

        self.result_template=MDBoxLayout(orientation='vertical', size_hint_y=None, spacing=20, padding=[10,10,10,10])
        self.result_template.bind(minimum_height=self.result_template.setter('height'))
        self.word=MDLabel(text="", font_style="main", font_size=20, halign='center', valign='middle', size_hint=(1, None), pos_hint={'center_x': 0.5}, theme_text_color="Custom", text_color=primarycolor)
        self.cefr_level=MDLabel(text="", font_style="Body2", halign='center', size_hint=(1, None), height=20, pos_hint={'center_x': 0.5}, theme_text_color="Custom", text_color=primarycolor)
        self.pronunciation_template=MDBoxLayout(size_hint_y=None, spacing=10, padding=[10,10,10,10], pos_hint={"center_x":0.5})
        self.pronunciation_template.bind(minimum_height=self.pronunciation_template.setter('height'))
        self.pronunciation=MDLabel(text="", font_style="main", font_size=18, halign='center', size_hint=(1, None), pos_hint={'center_x': 0.5}, theme_text_color="Custom", text_color=primarycolor)
        self.pronunciation_button=MDIconButton(icon="volume-high", theme_icon_color="Custom", icon_color=primarycolor, size_hint=(1, None), pos_hint={"center_x":0.5, "center_y": 0.25})
        self.definition=MDLabel(text="", font_style="Body1", halign='center', valign='middle', size_hint=(1, None), pos_hint={'center_x': 0.5}, theme_text_color="Custom", text_color=primarycolor)
        self.translation=MDLabel(text="", font_style="Body1", halign='center', valign='middle', size_hint=(1, None), pos_hint={'center_x': 0.5}, theme_text_color="Custom", text_color=primarycolor)
        self.word.bind(texture_size=self.word.setter('text_size'))
        self.word.bind(texture_size=self.word.setter('size'))
        self.cefr_level.bind(texture_size=self.cefr_level.setter('text_size'))
        self.cefr_level.bind(texture_size=self.cefr_level.setter('size'))
        self.pronunciation.bind(texture_size=self.pronunciation.setter('text_size'))
        self.pronunciation.bind(texture_size=self.pronunciation.setter('size'))
        self.definition.bind(texture_size=self.definition.setter('text_size'))
        self.definition.bind(texture_size=self.definition.setter('size'))
        self.translation.bind(texture_size=self.translation.setter('text_size'))
        self.translation.bind(texture_size=self.translation.setter('size'))      
        self.result_template.add_widget(self.word)
        self.result_template.add_widget(self.cefr_level)
        self.pronunciation_template.add_widget(self.pronunciation)
        self.pronunciation_template.add_widget(self.pronunciation_button)
        self.result_template.add_widget(self.pronunciation_template)
        self.result_template.add_widget(self.definition)

        self.synonyms=MDBoxLayout(orientation='vertical', size_hint_y=None, spacing=20, padding=[10,10,10,10])
        self.synonyms.bind(minimum_height=self.synonyms.setter('height'))

        temp_scroll_box=ScrollView(size_hint=(1, 1), pos_hint={"center_x": 0.5}, do_scroll_x=False)
        temp_scroll_box.add_widget(self.temp_box)
        container=MDCard(orientation="vertical", spacing=20, size_hint=(1,None), height=200, md_bg_color=btn)
        container.add_widget(temp_scroll_box)
        self.dialog = MDDialog(
            title="Gần đây",
            type="custom",
            content_cls=container,
            buttons=[
                MDFillRoundFlatButton(
                    text="Xóa",
                    md_bg_color=btn,
                    theme_text_color="Custom",
                    text_color=secondarycolor
                ),
                MDFillRoundFlatButton(
                    text="Đóng",
                    md_bg_color=btn,
                    theme_text_color="Custom",
                    text_color=secondarycolor
                )
            ],
            md_bg_color=boxbg
        )
        self.dialog.buttons[0].bind(on_release=self.clear_history)
        self.dialog.buttons[1].bind(on_release=self.dialog.dismiss)

        try:
            if int(width)>=900:
                self.noname.size_hint=(0.75, 1)
                self.one_box.add_widget(self.recent)
        except:
            pass

    def show_recent(self, *args):
        self.menu.dismiss()
        self.dialog.open()

    def clear_history(self, instance):
        global recent_search
        recent_search=[]
        self.temp_box.clear_widgets()
        self.recent_scrollview_box.clear_widgets()
        with open("func/setting/recent.txt", "w", encoding="utf-8"):
            pass

    def create_content_box(self, text, style=settings["homepage style"]):
        if style=="box":
            try:
                self.content_box=MDCard(md_bg_color=boxbg, padding=[10,10,10,10], size_hint=(1, None), pos_hint={"center_x":0.5})
                self.content_box.bind(minimum_height=self.content_box.setter('height'))
                self.tilte_and_description_box=MDBoxLayout(orientation='vertical', size_hint=(0.8,None))
                self.tilte_and_description_box.bind(minimum_height=self.tilte_and_description_box.setter('height'))
                self.result_head_label=MDLabel(text=text["word"]+" ("+text["type"].lower()+")"+f'\n/{eng_to_ipa.convert(text["word"])}/', font_style="main", font_size=18, size_hint=(0.9,None), pos_hint={"left":0}, theme_text_color="Custom", text_color=primarycolor)
                self.result_head_label.bind(texture_size=self.result_head_label.setter('text_size'))
                self.result_head_label.bind(texture_size=self.result_head_label.setter('size'))
                self.result_label=MDLabel(font_size=25, size_hint=(0.9,None), pos_hint={"left":1}, theme_text_color="Custom", text_color=primarycolor)
                if len(text["definition"])>30:
                    self.result_label.text=text["definition"][:50]+"..."
                else:
                    self.result_label.text=text["definition"]
                self.result_label.bind(texture_size=self.result_label.setter('text_size'))
                self.result_label.bind(texture_size=self.result_label.setter('size'))
                self.morebutton=MDFillRoundFlatButton(text="Xem thêm", size_hint=(None, None), pos_hint={"center_y":0.5}, md_bg_color=btn, theme_text_color="Custom", text_color=secondarycolor)
                self.tilte_and_description_box.add_widget(self.result_head_label)
                self.tilte_and_description_box.add_widget(self.result_label)
                self.content_box.add_widget(self.tilte_and_description_box)
                self.content_box.add_widget(self.morebutton)
                self.morebutton.bind(on_press=lambda instance: self.search_button_pressed(instance, text["word"]))
            except:
                pass
        
        elif style=="flashcard":
            try:
                self.content_box=MDCard(orientation="vertical", md_bg_color=boxbg, padding=[10,10,10,10], size_hint=(None, None), width=300, height=350, pos_hint={"center_x":0.5, "center_y":0.5})
                self.tilte_and_description_box=MDBoxLayout(orientation='vertical', size_hint=(0.8,0.75), pos_hint={"center_x":0.5})
                self.result_head_label=MDLabel(text=text["word"]+" ("+text["type"].lower()+")"+f'\n/{eng_to_ipa.convert(text["word"])}/', halign="center", font_style="main", font_size=18, size_hint=(1,0.4), pos_hint={"center_x":0.5}, theme_text_color="Custom", text_color=primarycolor)
                self.result_head_label.bind(texture_size=self.result_head_label.setter('text_size'))
                self.result_head_label.bind(texture_size=self.result_head_label.setter('size'))
                self.result_label=MDLabel(font_size=25, size_hint=(1,0.6), halign="center", valign="top", pos_hint={"center_x":0.5}, theme_text_color="Custom", text_color=primarycolor)
                if text["translation"]=="none":
                    self.result_label.text=text["definition"]
                else:
                    self.result_label.text=text["translation"]
                self.result_label.bind(texture_size=self.result_label.setter('text_size'))
                self.result_label.bind(texture_size=self.result_label.setter('size'))
                self.morebutton=MDFillRoundFlatButton(text="Xem thêm", size_hint=(None, None), pos_hint={"center_x":0.5}, md_bg_color=btn, theme_text_color="Custom", text_color=secondarycolor)
                self.tilte_and_description_box.add_widget(self.result_head_label)
                if text["level"]!="none":
                    self.cefr=MDLabel(text=text["level"], font_style="Body2", halign='center', size_hint=(1, None), pos_hint={'center_x': 0.5}, theme_text_color="Custom", text_color=primarycolor)
                    self.cefr.bind(texture_size=self.cefr.setter('text_size'))
                    self.cefr.bind(texture_size=self.cefr.setter('size'))
                    self.tilte_and_description_box.add_widget(self.cefr)
                self.tilte_and_description_box.add_widget(self.result_label)
                self.content_box.add_widget(self.tilte_and_description_box)
                self.content_box.add_widget(self.morebutton)
                self.morebutton.bind(on_press=lambda instance: self.search_button_pressed(instance, text["word"]))
            except:
                pass

        return self.content_box
        
    def refresh(self, instance, dict_, style=settings["homepage style"]):
        self.homebox.clear_widgets()
        if dict_==None:
            for i in range(10):
                self.homebox.add_widget(self.create_content_box(random.choice(SOD_word_list())))
            self.homebox.add_widget(self.refreshbutton)
        else:
            for i in dict_:
                self.homebox.add_widget(self.create_content_box(i, style))
    
    def menu_open(self, instance):
        menu_items = [
            {
                "text": "Đổi chủ đề",
                "theme_text_color": "Custom",
                "text_color": primarycolor,
                "trailing_icon": "weather-night",
                "theme_trailing_icon_color": "Custom",
                "trailing_icon_color": primarycolor,
                "on_release": lambda x="Dark mode": self.switch_theme(x)
            },
            {
                "text": "Cài đặt",
                "text_color": primarycolor,
                "trailing_icon": "cog",
                "theme_trailing_icon_color": "Custom",
                "trailing_icon_color": primarycolor,
                "on_release": lambda x="Setting": self.go_to_page_2(x)
            }
        ]
        if open("func/setting/theme.txt", encoding="utf-8").read()=="Dark":
            menu_items[0]["trailing_icon"]="weather-night"
        else:
            menu_items[0]["trailing_icon"]="white-balance-sunny"
        if Window.width<900:
            menu_items=menu_items[:1]+[{"text": "Gần đây",
                               "text_color": primarycolor,
                               "trailing_icon": "history",
                               "theme_trailing_icon_color": "Custom",
                               "trailing_icon_color": primarycolor,
                               "on_release": self.show_recent}]+menu_items[1:2]
        self.menu=MDDropdownMenu(
            caller=self.menubutton,
            items=menu_items,               
            ver_growth="up",
            md_bg_color=menubg,
            position="top"
        )
        self.menu.open()

    def home(self, instance):
        self.progress_bar.back_color=bg
        self.progress_bar.color=self.progress_bar.back_color
        self.noname.md_bg_color=bg
        self.homebutton.bind(on_press=self.home)
        self.scrollview.clear_widgets()
        if settings["homepage style"]=="flashcard":
            self.scrollview.do_scroll_x, self.scrollview.do_scroll_y=True,False
        self.scrollview.add_widget(self.homebox)

    def show_input(self, instance):
        self.box.clear_widgets()
        self.text_input = MDTextField(icon_left="magnify", icon_left_color_focus=btn, hint_text="Nhập từ cần tìm", line_color_normal=boxbg, line_color_focus=btn, hint_text_color=(115, 115, 115, 1), hint_text_color_focus=(0, 0, 0, 1), fill_color_normal=boxbg, text_color_focus=primarycolor, mode="round", size_hint=(0.75, None), pos_hint={'center_x': 0.5, 'center_y': 0.25}, height=30, multiline=False)
        self.box.add_widget(self.text_input)
        self.text_input.text=self.text
        self.text_input.bind(focus=self.hide_input)
        self.text_input.bind(text=self.quick_search)
        self.text_input.bind(on_text_validate=lambda instance: self.search_button_pressed(instance, self.text_input.text))
        
    def hide_input(self, instance, value):
        if ((len(self.text_input.text)==0) and (not value)) or self.signal:
            self.box.clear_widgets()
            self.taskbar.clear_widgets()
            self.taskbar.add_widget(self.homebutton)
            self.taskbar.add_widget(self.button)
            self.taskbar.add_widget(self.menubutton)
            self.button.bind(on_press=self.show_input)
            self.homebutton.bind(on_press=self.home)
            self.menubutton.bind(on_press=self.menu_open)
            self.box.add_widget(self.taskbar)
        self.signal=False

    def quick_search(self, instance, value):
        if self.search_thread:
            self.search_thread.cancel()
        if self.text_input.text!="":
            self.search_thread = threading.Timer(0.5, self.search_button_pressed, args=(instance, self.text_input.text))
            self.search_thread.start()
        else:
            self.home(instance)
        self.text=self.text_input.text

    def update_resultlabel(self, *args):
        self.result_box.remove_widget(self.resultlabel)
        self.resultlabel = MDLabel(text=self.resultlabel.text,
                                 font_style="H6",
                                 halign='center',
                                 valign='middle',
                                 size_hint=(1, None),
                                 pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                 height=30,
                                 theme_text_color="Custom",
                                 text_color=primarycolor)
        self.result_box.add_widget(self.resultlabel)
        self.resultlabel.bind(texture_size=self.resultlabel.setter('size'))

    def search_button_pressed(self, instance, input_text):
        try:
            self.dialog.dismiss()
        except:
            pass
        threading.Thread(target=self.search, args=(instance, input_text)).start()
        self.progress_bar.color=btn
        self.progress_bar.start()

    def search(self, instance, input_text):
        global result, dict_
        self.scrollview.do_scroll_x, self.scrollview.do_scroll_y=False, True
        input_text = word_detector(input_text)
        self.input_text=input_text
        result=[]
        included=[]
        dict_=[]
        for i in input_text:
            try:
                word = SOD(i.lower().replace("\n", " "), boost_performance=boost_performance_require, tu_dien=data_, word=source)
            except:
                result.append(i+": "+SOD(i.lower().replace("\n", " "), boost_performance=boost_performance_require, tu_dien=data_, word=source))
            else:
                if word in included:
                    continue
                try:
                    if word["translation"]!='none':
                        result.append(f'{word["word"].capitalize()} ({word["type"].lower()}): {word["definition"]}\n\nDịch: {word["translation"]}')
                        included.append(word)
                        dict_.append(word)
                    else:
                        result.append(f'{word["word"].capitalize()} ({word["type"].lower()}): {word["definition"]}')
                        included.append(word)
                        dict_.append(word)
                except:
                    result.append(word)
                    included.append(word)
                    dict_.append(word)

        Clock.schedule_once(self.update_UI)

    def update_UI(self, instance):
        global recent_search
        self.progress_bar.back_color=(boxbg)
        self.noname.md_bg_color=boxbg
        self.scrollview.do_scroll_x, self.scrollview.do_scroll_y=False, True
        self.scrollview.clear_widgets()
        self.scrollview.add_widget(self.result_box)
        self.result_box.clear_widgets()
        result_=SOD(" ".join(self.input_text).lower(), boost_performance=boost_performance_require, tu_dien=data_, word=source)
        if result==[]:
            result.append(result_)
        if len(result)<=1:
            if result_!="Không tìm thấy từ":
                self.word.text=result_["word"].capitalize()+f' ({result_["type"].lower()})'
                if result_["level"]!="none":
                    self.cefr_level.text=f"CEFR level: {result_['level']}"
                else:
                    self.cefr_level.text=""
                self.pronunciation_button.bind(on_release=lambda instance: self.pronounce(instance, result_["word"]))
                self.pronunciation.text=f'/{eng_to_ipa.convert(result_["word"])}/'
                self.definition.text=result_["definition"][:1].upper()+result_["definition"][1:]
                if result_["translation"]!="none":
                    self.translation.text="Dịch: "+result_["translation"]
                    self.result_template.remove_widget(self.translation)
                    self.result_template.add_widget(self.translation)
                else:
                    self.result_template.remove_widget(self.translation)
                self.result_box.remove_widget(self.result_template)
                self.result_box.add_widget(self.result_template)
                if result_ not in recent_search:
                    self.temp_box.add_widget(self.create_content_box(result_, style="box"), index=0)
                    self.recent_scrollview_box.add_widget(self.create_content_box(result_, style="box"), index=0)
                    recent_search=[result_]+recent_search
            
                synonyms = result_["synonyms"]
                self.synonyms.clear_widgets()
                head=MDLabel(text="Từ đồng nghĩa", halign="center", font_style="main", size_hint=(1,None), height=25, pos_hint={"center_x":0.5}, theme_text_color="Custom", text_color=primarycolor)
                if len(synonyms)!=0: self.synonyms.add_widget(head)
                count=0
                for i in range(len(synonyms)):
                    if count<=5:
                        temp=SOD(inp=synonyms[i].lower(), internet_required=False, tu_dien=data_, word=source)
                        if temp!="Không tìm thấy từ":
                            self.synonyms.add_widget(self.create_content_box(temp, style="box"))
                            count+=1
                    else:
                        break
                if (synonyms!=[]) and (count!=0):
                    self.result_box.add_widget(self.synonyms)
            else:
                self.resultlabel.text = "".join(result)
                self.result_box.remove_widget(self.resultlabel)
                self.result_box.add_widget(self.resultlabel)

        else:
            self.result_box.clear_widgets()
            self.structure_box=MDBoxLayout(size_hint=(1, None))
            for i in dict_:
                if i!="Không tìm thấy từ":
                    self.result_box.add_widget(self.create_content_box(i, style="box"))
                    if i not in recent_search:
                        self.recent_scrollview_box.add_widget(self.create_content_box(i, style="box"), index=0)
                        self.temp_box.add_widget(self.create_content_box(i, style="box"), index=0)
                        recent_search=[i]+recent_search
            self.result_box.add_widget(self.structure_box)
        if result!="Không tìm thấy từ":
            if grammar_structure_detector(self.text_input.text,"func/data/grammar.txt"):
                self.structure=MDLabel(text="Cấu trúc ngữ pháp đã nhận dạng:\n"+"\n".join(grammar_structure_detector(self.text_input.text,"func/data/grammar.txt")), font_style="H6", halign='center', valign='middle', size_hint=(1, None), pos_hint={'center_x': 0.5, 'center_y': 0.5}, theme_text_color="Custom", text_color=primarycolor)
                self.structure.bind(texture_size=self.resultlabel.setter('size'))
                self.structure_box.add_widget(self.structure)

        with open("func/setting/recent.txt", "w", encoding="utf-8") as fo:
            for i in recent_search:
                fo.write(f'{i["word"]}: {i["type"]}: {i["definition"]}: {i["translation"]}\n')
        self.progress_bar.color=self.progress_bar.back_color
        self.progress_bar.stop()

    def pronounce(self, instance, text):
        def run():
            engine.say(text)
            engine.runAndWait()
            engine.stop()

        threading.Thread(target=run).start()

    def switch_theme(self, *args):
        self.menu.dismiss()
        '''with open("func/setting/theme.txt", "r", encoding="utf-8") as theme:
            t=theme.readline().replace("\n","")
        with open("func/setting/theme.txt", "w", encoding="utf-8") as theme:
            if t=="Light":
                theme.write("Dark")
            else:
                theme.write("Light")
        with open("func/setting/color_theme.txt", "w", encoding="utf-8") as fo:
            fo.write("; ".join([", ".join([str(int(i*255)) for i in btn][:-1]),", ".join([str(int(i*255)) for i in menubg][:-1]),", ".join([str(int(i*255)) for i in boxbg][:-1]),", ".join([str(int(i*255)) for i in bg][:-1])]))
        MDApp.get_running_app().stop()'''

    def go_to_page_2(self, instance):
        self.menu.dismiss()
        sm.transition.direction = "left"
        sm.current = 'second'

    def on_double_tap(self, instance, *args):
        self.text=self.text_input.text
        self.signal=True
        self.hide_input(instance, False)

    def on_window_resize(self, window, width, height):
        if width>=900:
            self.noname.size_hint=(0.75, 1)
            try:
                self.one_box.add_widget(self.recent)
            except:
                pass
        else:
            self.noname.size_hint=(1, 1)
            try:
                self.one_box.remove_widget(self.recent)
            except:
                pass
            self.refresh(dict_=None, style="box")

        settings["size"]=str(Window.width)+" "+str(Window.height)

class FirstScreen(Screen):
    def __init__(self, **kwargs):
        super(FirstScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [10, 10, 10, 10]
        self.spacing = 20
        
        layout = MyLayout()
        self.add_widget(layout)

class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super(SecondScreen, self).__init__(**kwargs)
        setting_layout = SettingLayout()
        self.add_widget(setting_layout)

class MyApp(MDApp):
    def build(self):
        self.icon="func/Logo.ico"
        self.title="SODA Open Dictionary"
        sm.add_widget(FirstScreen(name='first'))
        sm.add_widget(SecondScreen(name='second'))
        return sm

sm = ScreenManager()

config()

if __name__ == '__main__':
    MyApp().run()
    set_new_config()