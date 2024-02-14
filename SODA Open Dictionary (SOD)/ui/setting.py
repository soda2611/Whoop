from init import *

class Setting(MDBoxLayout):
    def __init__(self, **kwargs):
        super(Setting, self).__init__(**kwargs)
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
            try:
                with open('func/pid.txt', 'r') as f:
                    pid = int(f.read())
                    os.kill(pid, signal.SIGTERM)
                os.remove('func/pid.txt')
            except:
                pass
        settings["waiting time"]=self.noti_time.text
        with open("func/setting/setting.txt", "w", encoding="utf-8") as fo:
            for i in settings:
                fo.write(f"{i}: {settings[i]}\n")
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir[:-3], "func\\noti.pyw")
        self.process = subprocess.Popen(["py", file_path], start_new_session=True, shell=True)
    
    def create_layout_preview(self, i):
        self.temp_box=MDCard(md_bg_color=(1,1,1,1), size_hint=(None, None), width=100, height=100, padding=[10, 10, 10, 10], spacing=20, ripple_behavior=True, on_press=lambda instance: self.change_homepage_layout(instance, "box"))
        if i=="box":
            self.temp_box.orientation="vertical"
        for j in range(2):
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
        sod_dir = settings["title"]
        icon_file = os.path.abspath(f"{sod_dir}/func/Logo.ico")
        shortcut_name = settings["title"]
        shortcut = os.path.join(r'C:/Users/%s/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup' %getpass.getuser() , shortcut_name + ".lnk")
        if noti_require: 
            self.noti_time.disabled=False
            settings["waiting time"]=self.noti_time.text
            with open("func/setting/setting.txt", "w", encoding="utf-8") as fo:
                for i in settings:
                    fo.write(f"{i}: {settings[i]}\n")
            status='bật'
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_dir[:-3], "func\\noti.pyw")
            self.process = subprocess.Popen(["py", file_path], start_new_session=True, shell=True)
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
                try:
                    with open('func/pid.txt', 'r') as f:
                        pid = int(f.read())
                        os.kill(pid, signal.SIGTERM)
                    os.remove('func/pid.txt')
                except:
                    pass
            os.remove(shortcut)
        notification = Notify(default_notification_message="Chế độ này sẽ gợi ý từ mới qua thông báo mỗi ngày để giúp bạn học từ tốt hơn",
                              default_notification_application_name=settings["title"],
                              default_notification_icon=settings["icon"],
                              default_notification_audio=settings["sound"])
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
