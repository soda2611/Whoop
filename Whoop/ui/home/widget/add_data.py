from ui import *

class add_data(MDBoxLayout):
    def __init__(self, **kwargs):
        super(add_data, self).__init__(**kwargs)
        self.orientation='vertical'
        self.size_hint_y=None
        self.spacing=20
        self.padding=[10,10,10,10]
        self.bind(minimum_height=self.setter('height'))
        self.label=MDLabel(text="Add data", font_style="H6", valign='middle', size_hint=(1, None), pos_hint={'center_x': 0.5}, theme_text_color="Custom", text_color=primarycolor, halign='center')
        self.word=MDTextField(hint_text="Word", hint_text_color=[0.75-i for i in primarycolor], hint_text_color_focus=primarycolor, text_color_focus=primarycolor, fill_color_normal=boxbg, size_hint=(1, None), pos_hint={'center_x': 0.5}, height=30*scale, multiline=False)
        self.cefr_level=MDTextField(hint_text="CEFR level", hint_text_color=[0.75-i for i in primarycolor], hint_text_color_focus=primarycolor, text_color_focus=primarycolor, fill_color_normal=boxbg, size_hint=(1, None), pos_hint={'center_x': 0.5}, height=30*scale, multiline=False)
        self.definition=MDTextField(hint_text="Definition", hint_text_color=[0.75-i for i in primarycolor], hint_text_color_focus=primarycolor, text_color_focus=primarycolor, fill_color_normal=boxbg, size_hint=(1, None), pos_hint={'center_x': 0.5}, height=30*scale, multiline=False)
        self.translation=MDTextField(hint_text="Translation", hint_text_color=[0.75-i for i in primarycolor], hint_text_color_focus=primarycolor, text_color_focus=primarycolor, fill_color_normal=boxbg, size_hint=(1, None), pos_hint={'center_x': 0.5}, height=30*scale, multiline=False)
        self.button=MDFillRoundFlatButton(text="Apply",size_hint=(None, None), pos_hint={"center_x":0.5, "center_y":0.5}, md_bg_color=btn, theme_text_color="Custom", text_color=secondarycolor)
        
        self.add_widget(self.label)
        self.add_widget(self.word)
        self.add_widget(self.cefr_level)
        self.add_widget(self.definition)
        self.add_widget(self.translation)
        self.add_widget(self.button)