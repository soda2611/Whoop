import ui as ui
from ui import *
from ui.setting.widget.noti_box import noti_box
from ui.setting.widget.change_layout import change_layout
from ui.setting.widget.change_palette import change_palette
from ui.setting.widget.change_fonts import change_fonts

class setting(MDBoxLayout):
    def __init__(self, **kwargs):
        super(setting, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [10, 10, 10, 10]
        self.spacing=20*scale
        self.md_bg_color=bg
        Window.bind(on_resize=self.on_window_resize)

        self.search_thread=None
        self.icon=MDIconButton(icon="check-circle", theme_icon_color="Custom", icon_color=primarycolor, size_hint=(None, None), pos_hint={"center_x": 0.5})
        self.got_check=None
        self.got_font_check=None
        self.touch_count=0
        self.timer = None
        self.back_button=MDIconButton(icon="arrow-left", size_hint=(None, None), pos_hint={"left": 0})
        self.back_button.bind(on_press=self.back)
        self.scrollview=ScrollView(size_hint=(1,1), do_scroll_x=False)
        self.personalize=MDBoxLayout(orientation="vertical", size_hint=(1,None), pos_hint={"center_x": 0.5}, spacing=20*scale)
        self.personalize.bind(minimum_height=self.personalize.setter('height'))
        self.scrollview.add_widget(self.personalize)
        self.noti_box=noti_box(self.noti, self.set_noti_time)
        self.internet_required_check_title=MDLabel(text="Chế độ Tối ưu hiệu suất", font_style="H6", size_hint=(1, None), height=30*scale, pos_hint={'center_x': 0.5, 'center_y': 0.5}, theme_text_color="Custom", text_color=primarycolor)
        self.internet_required_check=MDSwitch(icon_inactive="close", icon_active="check", icon_active_color=primarycolor, icon_inactive_color=secondarycolor, thumb_color_inactive=btn, thumb_color_active=boxbg, track_color_inactive=boxbg, track_color_active=btn)
        self.internet_required_check.active=settings["boost performance"]
        self.internet_required_check.bind(active=self.boost_performance)
        self.changelayout=MDLabel(text="Thay đổi bố cục trang chủ", font_style="H6", halign="left", size_hint=(1,None), height=30*scale, pos_hint={"center_x":0.5}, theme_text_color="Custom", text_color=primarycolor)
        self.layout_scroll=change_layout(self.create_layout_preview)
        self.changecolor=MDLabel(text="Cá nhân hóa với bảng màu", font_style="H6", halign="left", size_hint=(1,None), height=30*scale, pos_hint={"center_x":0.5}, theme_text_color="Custom", text_color=primarycolor)
        self.color_palette_scroll=change_palette(self.create_palette)
        self.change_fonts=MDLabel(text="Fonts", font_style="H6", halign="left", size_hint=(1,None), height=30*scale, pos_hint={"center_x":0.5}, theme_text_color="Custom", text_color=primarycolor)
        self.font_scroll=change_fonts(self.create_preview)
        self.color_palette_scroll.scroll_to(self.got_check)
        self.font_scroll.scroll_to(self.got_font_check)
        self.info=MDFillRoundFlatButton(text=f"Phiên bản: SOD {version}\nNgày phát hành: Unknown", font_style="Caption", halign="center", size_hint=(0.75,None), height=35*scale, pos_hint={"center_x": 0.5}, theme_text_color="Custom", text_color=primarycolor, md_bg_color=bg)
        self.info.bind(on_release=self.on_touch)
        self.dialog = MDDialog(
            title="Cài đặt liên quan đến cá nhân hóa sẽ được áp dụng khi bạn khởi động lại ứng dụng",
            type="alert",
            buttons=[
                MDFillRoundFlatButton(
                    text="Khởi động lại",
                    md_bg_color=btn,
                    theme_text_color="Custom",
                    text_color=secondarycolor,
                    on_press=self.restart
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
        self.dialog.buttons[1].bind(on_release=self.dialog.dismiss)

        '''self.notification=MDLabel(text="Bạn không thể thay đổi bất cứ cài đặt nào của ứng dụng trong phiên bản này. Vui lòng chờ phiên bản cập nhật tiếp theo.", font_style="H6", halign="center", size_hint=(0.75,1), pos_hint={"center_x": 0.5})
        self.add_widget(self.notification)'''

        self.add_widget(self.back_button)
        self.add_widget(self.scrollview)
        self.personalize.add_widget(self.noti_box.title)
        self.personalize.add_widget(self.noti_box)
        self.personalize.add_widget(self.internet_required_check_title)
        self.personalize.add_widget(self.internet_required_check)
        self.personalize.add_widget(self.changelayout)
        self.personalize.add_widget(self.layout_scroll)
        self.personalize.add_widget(self.changecolor)
        self.personalize.add_widget(self.color_palette_scroll)
        self.personalize.add_widget(self.change_fonts)
        self.personalize.add_widget(self.font_scroll)
        self.add_widget(self.info)

    def restart(self, instance):
        pid=int(open("func/main_pid.txt", encoding="utf-8").read())
        set_new_config()
        subprocess.Popen(["py", "UI.py"], start_new_session=True)
        os.kill(pid, signal.SIGTERM)

    def run_noti(self, instance):
        if os.path.exists('func/pid.txt'):
            try:
                with open('func/pid.txt', 'r') as f:
                    pid = int(f.read())
                    os.kill(pid, signal.SIGTERM)
                os.remove('func/pid.txt')
            except:
                pass
        settings["waiting time"]=self.noti_box.noti_time.text
        with open("func/setting/setting.txt", "w", encoding="utf-8") as fo:
            for i in settings:
                fo.write(f"{i}: {settings[i]}\n")
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir[:-11], "func\\noti.pyw")
        self.process = subprocess.Popen(["py", file_path], start_new_session=True, shell=True)

    def set_noti_time(self, instance, time):
        if self.search_thread:
            self.search_thread.cancel()
        self.search_thread = threading.Timer(0.5, self.run_noti, args=(instance,))
        self.search_thread.start()

    def noti(self, instance, value):
        global noti_require
        noti_require= not noti_require
        ui.settings["notification"]=str(noti_require)
        shortcut_name = settings["title"]
        shortcut = os.path.join(r'C:/Users/%s/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup' %getpass.getuser() , shortcut_name + ".lnk")
        if noti_require: 
            self.noti_box.noti_time.disabled=False
            settings["waiting time"]=self.noti_box.noti_time.text
            status="bật"
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_dir[:-11], "func\\noti.pyw")
            self.process = subprocess.Popen(["py", file_path], start_new_session=True, shell=True)
        else:
            self.noti_box.noti_time.disabled=True
            status='tắt'
            if os.path.exists('func/pid.txt'):
                try:
                    with open('func/pid.txt', 'r') as f:
                        pid = int(f.read())
                        os.kill(pid, signal.SIGTERM)
                    os.remove('func/pid.txt')
                except:
                    pass
            if os.path.exists(shortcut):
                os.remove(shortcut)
        notification = Notify(default_notification_message="Chế độ này sẽ gợi ý từ mới qua thông báo mỗi ngày để giúp bạn học từ tốt hơn",
                              default_notification_application_name=settings["title"],
                              default_notification_icon=settings["icon"],
                              default_notification_audio=settings["sound"])
        notification.title = f"Gợi ý từ qua thông báo đã {status}"
        notification.send()
    
    def create_layout_preview(self, i):
        self.temp_box=MDCard(md_bg_color=(1,1,1,1), size_hint=(None, None), width=100*scale, height=100*scale, padding=[10*scale, 10*scale, 10*scale, 10*scale], spacing=20*scale, ripple_behavior=True, on_press=lambda instance: self.change_homepage_layout(instance, "box"))
        self.temp_box.radius=[i*scale for i in self.temp_box.radius]
        if i=="box":
            self.temp_box.orientation="vertical"
        for j in range(2):
            box=MDCard(width=75*scale, height=22.5*scale, pos_hint={'center_x': 0.5}, md_bg_color=boxbg)
            box.radius=[i*scale for i in box.radius]
            if i=="flashcard":
                box.orientation="vertical"
            self.temp_box.add_widget(box)
        self.temp_box.bind(on_press=lambda instance: self.change_homepage_layout(instance, i))
        
        return self.temp_box

    def change_homepage_layout(self, instance, style):
        ui.settings["homepage style"]=style
        self.dialog.open()
        
    def create_palette(self, i):
        self.color=MDCard(md_bg_color=(1,1,1,1), orientation="vertical", size_hint=(None, None), width=50*scale, height=200*scale, pos_hint={"center_x": 0.5}, padding=[10*scale, 10*scale, 10*scale, 10*scale], ripple_behavior=True)
        self.color.radius=[i*scale for i in self.color.radius]
        theme=[]
        for j in i:
            theme.append([int(j[0])/255,int(j[1])/255,int(j[2])/255, 1])
        for j in i[:4]:
            self.color1=MDBoxLayout(md_bg_color=(int(j[0])/255,int(j[1])/255,int(j[2])/255, 1),size_hint=(1,0.25), pos_hint={"center_x":0.5})
            self.color.add_widget(self.color1)
        if [[str(int(i*255)) for i in bg[:-1]], [str(int(i*255)) for i in boxbg[:-1]], [str(int(i*255)) for i in menubg[:-1]], [str(int(i*255)) for i in btn[:-1]]]==i[:4]:
            self.color.height=250*scale
            self.color.add_widget(self.icon)
            self.got_check=self.color
        self.color.bind(on_press=lambda instance: self.change_color_theme(instance, theme[0], theme[1], theme[2], theme[3], theme[4], theme[5]))

        return self.color

    def change_color_theme(self, instance, new_bg, new_boxbg, new_menubg, new_btn, new_primarycolor, new_secondarycolor):
        self.got_check.remove_widget(self.icon)
        self.got_check.height=200*scale
        self.got_check=instance
        instance.height=250*scale
        instance.add_widget(self.icon)
        self.color_palette_scroll.scroll_to(self.got_check)
        ui.settings["current palette"]="; ".join([", ".join([str(int(i*255)) for i in new_bg][:-1]),", ".join([str(int(i*255)) for i in new_boxbg][:-1]),", ".join([str(int(i*255)) for i in new_menubg][:-1]),", ".join([str(int(i*255)) for i in new_btn][:-1]), ", ".join([str(int(i*255)) for i in new_primarycolor][:-1]), ", ".join([str(int(i*255)) for i in new_secondarycolor][:-1])])
        self.dialog.open()

    def create_preview(self, i):
        self.font=MDFillRoundFlatIconButton(text=i, theme_icon_color='Custom', md_bg_color=btn, theme_text_color="Custom", text_color=secondarycolor, font_name=f"func/setting/fonts/{i}.ttf", font_size=17*scale)
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
        ui.settings["fonts"]=i
        self.dialog.open()

    def boost_performance(self, instance, value):
        ui.settings["boost performance"]=not settings["boost performance"]

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
                  height=25*scale,
                  pos_hint={"center_x": 0.5},
                  theme_text_color="Custom",
                  text_color=primarycolor)
        self.cre.bind(texture_size=self.cre.setter('text_size'))
        self.cre.bind(texture_size=self.cre.setter('size'))
        self.temp_scroll_box=ScrollView(size_hint=(1, 1), pos_hint={"center_x": 0.5}, do_scroll_x=False)
        self.temp_scroll_box.add_widget(self.cre)
        self.container=MDCard(orientation="vertical", spacing=20*scale, size_hint=(1,None), height=200*scale, padding=[10*scale, 10*scale, 10*scale, 10*scale])
        self.container.radius=[i*scale for i in self.container.radius]
        self.container.add_widget(self.temp_scroll_box)
        self.credit=MDDialog(
        title="Thư cảm ơn từ Nhà phát triển SODA Open Dictionary",
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

    def on_window_resize(self, window, width, height):
        if (width == Window.minimum_width) and (height == Window.minimum_height):
            self.color_palette_scroll.pos_hint={"center_x": 0.5}
        else:
            self.color_palette_scroll.pos_hint={"x": 0}
