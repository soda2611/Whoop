from ui import *

class content_box(MDCard):
    def __init__(self, text, **kwargs):
        super(content_box, self).__init__(**kwargs)
        self.md_bg_color=boxbg
        self.padding=[dp(10),dp(10),dp(10),dp(10)]
        self.size_hint=(1, None)
        self.pos_hint={"center_x":0.5}
        self.radius=[dp(i) for i in self.radius]
        self.bind(minimum_height=self.setter('height'))
        self.tilte_and_description_box=MDBoxLayout(orientation='vertical', size_hint=(0.8,None))
        self.tilte_and_description_box.bind(minimum_height=self.tilte_and_description_box.setter('height'))
        self.result_head_label=MDLabel(text=text["word"]+" ("+text["type"].lower()+")"+f'\n/{eng_to_ipa.convert(text["word"])}/', font_style="main", font_size=dp(18), size_hint=(0.9,None), pos_hint={"left":0}, theme_text_color="Custom", text_color=primarycolor)
        self.result_head_label.bind(texture_size=self.result_head_label.setter('text_size'))
        self.result_head_label.bind(texture_size=self.result_head_label.setter('size'))
        self.result_label=MDLabel(font_size=dp(25), size_hint=(0.9,None), pos_hint={"left":1}, theme_text_color="Custom", text_color=primarycolor)
        if len(text["definition"])>50:
            self.result_label.text=text["definition"][:50]+"..."
        else:
            self.result_label.text=text["definition"]
        self.result_label.bind(texture_size=self.result_label.setter('text_size'))
        self.result_label.bind(texture_size=self.result_label.setter('size'))
        self.tilte_and_description_box.add_widget(self.result_head_label)
        self.tilte_and_description_box.add_widget(self.result_label)
        self.add_widget(self.tilte_and_description_box)
        
class content_box_(MDCard):
     def __init__(self, text, **kwargs):
        super(content_box_, self).__init__(**kwargs)
        self.md_bg_color=boxbg
        self.padding=[dp(10),dp(10),dp(10),dp(10)]
        self.size_hint=(1, None)
        self.pos_hint={"center_x":0.5}
        self.radius=[dp(i) for i in self.radius]
        self.bind(minimum_height=self.setter('height'))
        self.tilte_and_description_box=MDBoxLayout(orientation='vertical', size_hint=(0.8,None))
        self.tilte_and_description_box.bind(minimum_height=self.tilte_and_description_box.setter('height'))
        self.result_head_label=MDLabel(text=text["word"], font_style="main", font_size=dp(18), size_hint=(0.9,None), pos_hint={"left":0}, theme_text_color="Custom", text_color=primarycolor)
        self.result_head_label.bind(texture_size=self.result_head_label.setter('text_size'))
        self.result_head_label.bind(texture_size=self.result_head_label.setter('size'))
        self.result_label=MDLabel(font_size=dp(25), size_hint=(0.9,None), pos_hint={"left":1}, theme_text_color="Custom", text_color=primarycolor)
        self.result_label.text=text["definition"]
        self.result_label.bind(texture_size=self.result_label.setter('text_size'))
        self.result_label.bind(texture_size=self.result_label.setter('size'))
        self.tilte_and_description_box.add_widget(self.result_head_label)
        self.tilte_and_description_box.add_widget(self.result_label)
        self.add_widget(self.tilte_and_description_box)