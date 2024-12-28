from ui import *

synonyms_list=[]
antonyms_list=[]

class add_data(MDBoxLayout):
    def __init__(self, **kwargs):
        super(add_data, self).__init__(**kwargs)
        self.orientation='vertical'
        self.size_hint_y=None
        self.spacing=dp(20)
        self.padding=[dp(10), dp(10), dp(10), dp(10)]
        self.bind(minimum_height=self.setter('height'))
        
        self.synonym_container=MDTextField(hint_text="Type here", line_color_normal=boxbg, line_color_focus=menubg, hint_text_color=[0.75-i for i in primarycolor], hint_text_color_focus=primarycolor, text_color_focus=primarycolor, fill_color_normal=boxbg, mode="round", size_hint=(1, None), pos_hint={'center_x': 0.5}, height=dp(30), multiline=False)
        self.synonym_container.bind(on_text_validate=self.add_synonym)
        self.antonym_container=MDTextField(hint_text="Type here", line_color_normal=boxbg, line_color_focus=menubg, hint_text_color=[0.75-i for i in primarycolor], hint_text_color_focus=primarycolor, text_color_focus=primarycolor, fill_color_normal=boxbg, mode="round", size_hint=(1, None), pos_hint={'center_x': 0.5}, height=dp(30), multiline=False)
        self.antonym_container.bind(on_text_validate=self.add_antonym)

        self.synonym_dialog=MDDialog(
            title=f"Add synonym",
            type="custom",
            content_cls=self.synonym_container,
            buttons=[
                MDFillRoundFlatButton(
                    text="Apply",
                    md_bg_color=btn,
                    theme_text_color="Custom",
                    text_color=secondarycolor
                ),
                MDFillRoundFlatButton(
                    text="Cancel",
                    md_bg_color=btn,
                    theme_text_color="Custom",
                    text_color=secondarycolor
                )],
            md_bg_color=boxbg
        )
        self.synonym_dialog.buttons[0].bind(on_release=self.add_synonym)
        self.synonym_dialog.buttons[1].bind(on_release=self.synonym_dialog.dismiss)

        self.antonym_dialog=MDDialog(
            title=f"Add antonym",
            type="custom",
            content_cls=self.antonym_container,
            buttons=[
                MDFillRoundFlatButton(
                    text="Apply",
                    md_bg_color=btn,
                    theme_text_color="Custom",
                    text_color=secondarycolor
                ),
                MDFillRoundFlatButton(
                    text="Cancel",
                    md_bg_color=btn,
                    theme_text_color="Custom",
                    text_color=secondarycolor
                )],
            md_bg_color=boxbg
        )
        self.antonym_dialog.buttons[0].bind(on_release=self.add_antonym)
        self.antonym_dialog.buttons[1].bind(on_release=self.antonym_dialog.dismiss)
        
        self.label=MDLabel(text="Add data", font_style="H6", valign='middle', size_hint=(1, None), pos_hint={'center_x': 0.5}, theme_text_color="Custom", text_color=primarycolor, halign='center')
        self.word=MDTextField(hint_text="Word", hint_text_color=[0.75-i for i in primarycolor], hint_text_color_focus=primarycolor, text_color_focus=primarycolor, fill_color_normal=boxbg, line_color_focus=btn, size_hint=(1, None), pos_hint={'center_x': 0.5}, height=dp(30), multiline=False)
        self.type=MDTextField(hint_text="Type", hint_text_color=[0.75-i for i in primarycolor], hint_text_color_focus=primarycolor, text_color_focus=primarycolor, fill_color_normal=boxbg, line_color_focus=btn, size_hint=(1, None), pos_hint={'center_x': 0.5}, height=dp(30), multiline=False)
        self.definition=MDTextField(hint_text="Definition", hint_text_color=[0.75-i for i in primarycolor], hint_text_color_focus=primarycolor, text_color_focus=primarycolor, fill_color_normal=boxbg, line_color_focus=btn, size_hint=(1, None), pos_hint={'center_x': 0.5}, height=dp(30), multiline=True)
        self.add_synonyms=add_synonyms()
        self.add_synonym_button=MDFillRoundFlatIconButton(text="Add synonym", icon="plus-circle", theme_icon_color='Custom', md_bg_color=btn, theme_text_color="Custom", icon_color=secondarycolor,  text_color=secondarycolor, on_press=self.synonym_dialog.open)
        self.add_synonyms.synonyms_list.add_widget(self.add_synonym_button)
        self.add_antonyms=add_antonyms()
        self.add_antonym_button=MDFillRoundFlatIconButton(text="Add antonym", icon="plus-circle", theme_icon_color='Custom', md_bg_color=btn, theme_text_color="Custom", icon_color=secondarycolor,  text_color=secondarycolor, on_press=self.antonym_dialog.open)
        self.add_antonyms.antonyms_list.add_widget(self.add_antonym_button)
        
        self.button=MDFillRoundFlatButton(text="Apply",size_hint=(None, None), pos_hint={"center_x":0.5, "center_y":0.5}, md_bg_color=btn, theme_text_color="Custom", text_color=secondarycolor, on_press=self.add_data)
        
        self.add_widget(self.label)
        self.add_widget(self.word)
        self.add_widget(self.type)
        self.add_widget(self.definition)
        self.add_widget(self.add_synonyms)
        self.add_widget(self.add_antonyms)
        self.add_widget(self.button)
        
    def add_antonym(self, instance):
        global antonyms_list
        while "  " in self.antonym_container.text:
            self.antonym_container.text=self.antonym_container.text.replace("  "," ")
        self.antonym_container.text=self.antonym_container.text.strip()
        if self.antonym_container.text not in antonyms_list and self.antonym_container.text!="":
            antonyms_list.append(self.antonym_container.text)
            self.add_antonyms.antonyms_list.add_widget(self.create_chips(self.antonym_container.text, on_press=self.remove_antonym))
          
        self.antonym_container.text=""
        self.antonym_dialog.dismiss()

    def add_synonym(self, instance):
        global synonyms_list
        while "  " in self.synonym_container.text:
            self.synonym_container.text=self.synonym_container.text.replace("  "," ")
        self.synonym_container.text=self.synonym_container.text.strip()
        if self.synonym_container.text not in synonyms_list and self.synonym_container.text!="":
            synonyms_list.append(self.synonym_container.text)
            self.add_synonyms.synonyms_list.add_widget(self.create_chips(self.synonym_container.text, on_press=self.remove_synonym))
          
        self.synonym_container.text=""
        self.synonym_dialog.dismiss()

    def remove_antonym(self, instance):
        global antonyms_list
        antonyms_list.remove(instance.text)
        self.add_antonyms.antonyms_list.remove_widget(instance)
        
    def remove_synonym(self, instance):
        global synonyms_list
        synonyms_list.remove(instance.text)
        self.add_synonyms.synonyms_list.remove_widget(instance)
        
    global synonyms_list, antonyms_list
        if self.word.text and self.type.text:
            with open("func/data/tu_dien_nguon.txt", 'r', encoding="utf-8") as file:
                data = eval(file.read())
            with open("func/data/source.txt", 'r', encoding="utf-8") as file:
                source = eval(file.read())
            if self.definition.text:
                if self.word.text not in data:
                    data[self.word.text]={self.type.text:{
                        "definition": self.definition.text,
                        "synonyms": synonyms_list,
                        "antonyms": antonyms_list,
                        "word": self.word.text,
                        "type": self.type.text
                    }}
                else:
                    data[self.word.text][self.type.text]={
                                "definition": self.definition.text,
                                "synonyms": synonyms_list,
                                "antonyms": antonyms_list,
                                "word": self.word.text,
                                "type": self.type.text
                            }
            else:
                del data[self.word.text][self.type.text]
                if not data[self.word.text]:
                    del data[self.word.text]
                    source.remove(self.word.text)
            if self.word.text not in source:
                source.append(self.word.text)
            with open("func/data/tu_dien_nguon.txt", 'w', encoding="utf-8") as file:
                file.write(json.dumps(data, ensure_ascii=False, indent=4))
            with open("func/data/source.txt", 'w', encoding="utf-8") as file:
                file.write(str(source))
            self.word.text = self.type.text = self.definition.text = ""
            self.add_synonyms.synonyms_list.clear_widgets()
            self.add_synonyms.synonyms_list.add_widget(self.add_synonym_button)
            self.add_antonyms.antonyms_list.clear_widgets()
            self.add_antonyms.antonyms_list.add_widget(self.add_antonym_button)
            synonyms_list = []
            antonyms_list = []
            
    def create_chips(self, text, on_press):
        return MDFillRoundFlatButton(text=text, theme_icon_color='Custom', md_bg_color=btn, theme_text_color="Custom", text_color=secondarycolor, on_press=on_press)
        
class add_synonyms(ScrollView):
    def __init__(self, **kwargs):
        super(add_synonyms, self).__init__(**kwargs)
        self.do_scroll_y=False
        self.size_hint=(1, None)
        self.height=dp(50)
        self.synonyms_list=MDBoxLayout(size_hint=(None, 1), pos_hint={"center_x": 0.5}, spacing=dp(20), padding=[dp(10), dp(10), dp(10), dp(10)])
        self.synonyms_list.height=dp(self.synonyms_list.height)
        self.synonyms_list.bind(minimum_width=self.synonyms_list.setter('width'))
        self.add_widget(self.synonyms_list)

class add_antonyms(ScrollView):
    def __init__(self, **kwargs):
        super(add_antonyms, self).__init__(**kwargs)
        self.do_scroll_y=False
        self.size_hint=(1, None)
        self.height=dp(50)
        self.antonyms_list=MDBoxLayout(size_hint=(None, 1), pos_hint={"center_x": 0.5}, spacing=dp(20), padding=[dp(10), dp(10), dp(10), dp(10)])
        self.antonyms_list.height=dp(self.antonyms_list.height)
        self.antonyms_list.bind(minimum_width=self.antonyms_list.setter('width'))
        self.add_widget(self.antonyms_list)
