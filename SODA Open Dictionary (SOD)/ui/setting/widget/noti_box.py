from ui import *

class noti_box(MDBoxLayout):
    def __init__(self, noti, set_noti_time, **kwargs):
        super(noti_box, self).__init__(**kwargs)
        self.size_hint=(1, None)
        self.height=50*scale
        self.pos_hint={'center_x': 0.5, 'center_y': 0.5}
        self.spacing=20*scale
        self.switch_box=MDBoxLayout(size_hint=(0.25, None), height=50*scale, pos_hint={'center_x': 0.5, 'center_y': 0.5}, spacing=20*scale)
        self.time_value_box=MDBoxLayout(size_hint=(0.75, None), height=50*scale, pos_hint={'left': 0.9, 'center_y': 0.8}, spacing=20*scale)
        self.title=MDLabel(text="Gợi ý từ mới qua thông báo", font_style="H6", size_hint=(1, None), height=30*scale, pos_hint={'center_x': 0.5, 'center_y': 0.5}, theme_text_color="Custom", text_color=primarycolor)
        self.check=MDSwitch(icon_inactive="close", icon_active="check", icon_active_color=primarycolor, icon_inactive_color=secondarycolor, thumb_color_inactive=btn, thumb_color_active=boxbg, track_color_inactive=boxbg, track_color_active=btn)
        self.check.active=noti_require
        self.check.bind(active=noti)
        self.time_title=MDLabel(text="Thời gian chờ thông báo", font_style="Body2", halign="right", size_hint=(0.5, None), pos_hint={"right": 0.7}, height=30*scale, theme_text_color="Custom", text_color=primarycolor)        
        self.noti_time=MDTextField(icon_left="clock", icon_left_color_focus=btn, text=settings["waiting time"], line_color_normal=(115, 115, 115, 1), line_color_focus=(0, 0, 0, 1), hint_text_color=(115, 115, 115, 1), hint_text_color_focus=(0, 0, 0, 1), text_color_focus=(0, 0, 0, 1), fill_color_normal=(1, 1, 1, 1), mode="round", size_hint=(None, None), pos_hint={"right": 0.75}, width=100*scale, height=30*scale, multiline=False, disabled=not noti_require)
        self.noti_time.bind(text=set_noti_time)
        self.add_widget(self.switch_box)
        self.switch_box.add_widget(self.check)
        self.add_widget(self.time_value_box)
        self.time_value_box.add_widget(self.time_title)
        self.time_value_box.add_widget(self.noti_time)