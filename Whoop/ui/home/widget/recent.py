from ui import *

class recent(MDCard):
    def __init__(self, create_content_box, clear_history, radius, **kwargs):
        super(recent, self).__init__(**kwargs)
        self.orientation='vertical'
        self.md_bg_color=boxbg
        self.size_hint=(0.45, 1)
        self.width=dp(250)
        self.pos_hint={'center_x': 0.5, 'center_y': 0.5}
        self.padding=[dp(10), dp(10), dp(10), dp(10)]
        self.spacing=dp(20)
        self.radius=[dp(i) for i in radius]
        self.recent_label=MDLabel(text="Gần đây", font_style="H6", halign="center", size_hint=(1,None), height=dp(25), pos_hint={"center_x": 0.5}, theme_text_color="Custom", text_color=primarycolor)
        self.label=MDLabel(text="Lịch sử tìm kiếm trống", font_style="Body1", halign="center", size_hint=(1,1), pos_hint={"center_x": 0.5, "center_y": 0.5}, theme_text_color="Custom", text_color=primarycolor)
        self.recent_scrollview = ScrollView(size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5}, do_scroll_x=False)
        self.container=MDBoxLayout(size_hint=(1, 1), pos_hint={"center_x":0.5})
        self.action_box=MDBoxLayout(size_hint=(1, None), height=dp(20), spacing=20, pos_hint={"center_x":0.5})
        self.clear_action=MDFillRoundFlatButton(text="Xoá", md_bg_color=btn, pos_hint={"center_x": 0.5}, theme_text_color="Custom", text_color=secondarycolor)
        self.recent_scrollview_box=MDBoxLayout(orientation='vertical', size_hint=(1, None), spacing=dp(20))
        self.recent_scrollview_box.bind(minimum_height=self.recent_scrollview_box.setter('height'))
        self.add_widget(self.recent_label)
        self.add_widget(self.container)
        self.add_widget(self.clear_action)
        self.recent_scrollview.add_widget(self.recent_scrollview_box)
        self.clear_action.bind(on_release=clear_history)

class recent_(MDCard):
    def __init__(self, create_content_box, clear_history, radius, **kwargs):
        super(recent_, self).__init__(**kwargs)
        self.orientation='vertical'
        self.md_bg_color=boxbg
        self.size_hint=(1, 1)
        self.pos_hint={'center_x': 0.5, 'center_y': 0.5}
        self.padding=[dp(10), dp(10), dp(10), dp(10)]
        self.spacing=dp(20)
        self.radius=radius
        self.label=MDLabel(text="Lịch sử tìm kiếm trống", font_style="Body1", halign="center", size_hint=(1,1), pos_hint={"center_x": 0.5, "center_y": 0.5}, theme_text_color="Custom", text_color=primarycolor)
        self.recent_label=MDLabel(text="Gần đây", font_style="H6", halign="center", size_hint=(1,None), height=dp(25), pos_hint={"center_x": 0.5}, theme_text_color="Custom", text_color=primarycolor)
        self.recent_scrollview = ScrollView(size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5}, do_scroll_x=False)
        self.container=MDBoxLayout(size_hint=(1, 1), pos_hint={"center_x":0.5})
        self.action_box=MDBoxLayout(size_hint=(1, None), height=dp(20), spacing=dp(20), pos_hint={"center_x":0.5})
        self.clear_action=MDFillRoundFlatButton(text="Xoá", md_bg_color=btn, pos_hint={"center_x": 0.5}, theme_text_color="Custom", text_color=secondarycolor)
        self.recent_scrollview_box=MDBoxLayout(orientation='vertical', size_hint=(1, None), spacing=dp(20))
        self.recent_scrollview_box.bind(minimum_height=self.recent_scrollview_box.setter('height'))
        self.add_widget(self.recent_label)
        self.add_widget(self.container)
        self.add_widget(self.clear_action)
        self.recent_scrollview.add_widget(self.recent_scrollview_box)
        self.clear_action.bind(on_release=clear_history)
