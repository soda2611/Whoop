from ui import *

class favwordlist(MDCard):
    def __init__(self, **kwargs):
        super(favwordlist, self).__init__(**kwargs)
        self.orientation='vertical'
        self.md_bg_color=boxbg
        self.size_hint=(1, 1)
        self.width=dp(250)
        self.pos_hint={'center_x': 0.5, 'center_y': 0.5}
        self.padding=[dp(10), dp(10), dp(10), dp(10)]
        self.spacing=dp(20)
        self.radius=[dp(25), dp(25), dp(25), dp(25)]
        self.label=MDLabel(text="Danh sách yêu thích trống", font_style="Body1", halign="center", size_hint=(1,1), pos_hint={"center_x": 0.5, "center_y": 0.5}, theme_text_color="Custom", text_color=primarycolor)
        self.fav_scrollview = ScrollView(size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5}, do_scroll_x=False)
        self.container=MDBoxLayout(size_hint=(1, 1), pos_hint={"center_x":0.5})
        self.action_box=MDBoxLayout(size_hint=(1, None), height=dp(20), spacing=20, pos_hint={"center_x":0.5})
        self.fav_scrollview_box=MDBoxLayout(orientation="vertical", size_hint=(1, None), spacing=dp(20))
        self.fav_scrollview_box.bind(minimum_height=self.fav_scrollview_box.setter('height'))
        self.add_widget(self.container)
        self.fav_scrollview.add_widget(self.fav_scrollview_box)

class folder(MDCard):
    def __init__(self, text, folder_len, **kwargs):
        super(folder, self).__init__(**kwargs)
        self.md_bg_color=boxbg
        self.padding=[dp(10),dp(10),dp(10),dp(10)]
        self.size_hint=(1, None)
        self.pos_hint={"center_x":0.5}
        self.radius=[dp(i) for i in self.radius]
        self.bind(minimum_height=self.setter('height'))
        self.tilte_and_description_box=MDBoxLayout(orientation='vertical', size_hint=(0.8,None))
        self.tilte_and_description_box.bind(minimum_height=self.tilte_and_description_box.setter('height'))
        self.result_head_label=MDLabel(text=text, font_style="main", font_size=dp(18), size_hint=(0.9,None), pos_hint={"left":0}, theme_text_color="Custom", text_color=primarycolor)
        self.result_head_label.bind(texture_size=self.result_head_label.setter('text_size'))
        self.result_head_label.bind(texture_size=self.result_head_label.setter('size'))
        self.result_label=MDLabel(font_size=dp(25), size_hint=(0.9,None), pos_hint={"left":1}, theme_text_color="Custom", text_color=primarycolor)
        self.result_label.text=folder_len
        self.result_label.bind(texture_size=self.result_label.setter('text_size'))
        self.result_label.bind(texture_size=self.result_label.setter('size'))
        self.tilte_and_description_box.add_widget(self.result_head_label)
        self.tilte_and_description_box.add_widget(self.result_label)
        self.add_widget(self.tilte_and_description_box)