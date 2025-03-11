from ui import *

class result_template(MDBoxLayout):
    def __init__(self, **kwargs):
        super(result_template, self).__init__(**kwargs)
        self.orientation='vertical'
        self.size_hint_y=None
        self.spacing=dp(20)
        self.padding=[dp(10), dp(10), dp(10), dp(10)]
        self.bind(minimum_height=self.setter('height'))
        self.word=MDLabel(text="", font_style="main", font_size=dp(20), halign='center', valign='middle', size_hint=(1, None), pos_hint={'center_x': 0.5, "center_y": 0.5}, theme_text_color="Custom", text_color=primarycolor)
        self.pronunciation_template=MDBoxLayout(size_hint_y=None, spacing=dp(10), padding=[dp(10), dp(10), dp(10), dp(10)], pos_hint={"center_x":0.5})
        self.pronunciation_template.bind(minimum_height=self.pronunciation_template.setter('height'))
        self.pronunciation=MDLabel(text="", font_style="main", font_size=dp(18), halign='center', size_hint=(1, None), pos_hint={'center_x': 0.5}, theme_text_color="Custom", text_color=primarycolor)
        self.pronunciation_button=MDIconButton(icon="volume-high", theme_icon_color="Custom", icon_color=primarycolor, size_hint=(1, None), pos_hint={"center_x":0.5, "center_y": 0.25})
        self.definition=MDLabel(text="", font_style="Body1", valign='middle', size_hint=(1, None), pos_hint={'center_x': 0.5}, theme_text_color="Custom", text_color=primarycolor, allow_copy=True)
        self.word.bind(texture_size=self.word.setter('text_size'))
        self.word.bind(texture_size=self.word.setter('size'))
        self.pronunciation.bind(texture_size=self.pronunciation.setter('text_size'))
        self.pronunciation.bind(texture_size=self.pronunciation.setter('size'))
        self.definition.bind(texture_size=self.definition.setter('text_size'))
        self.definition.bind(texture_size=self.definition.setter('size'))
        self.pronunciation_template.add_widget(self.pronunciation)
        self.pronunciation_template.add_widget(self.pronunciation_button)
        self.add_widget(self.pronunciation_template)
        self.add_widget(self.definition)

class translate_result_template(MDCard):
    def __init__(self, **kwargs):
        super(translate_result_template, self).__init__(**kwargs)
        self.orientation='vertical'
        self.size_hint=(1, 1)
        self.md_bg_color=[0, 0, 0, 0]
        self.spacing=dp(20)
        self.padding=[dp(10), dp(10), dp(10), dp(10)]
        self.translate_thread=None
        self.translate_event=threading.Event()
        self.bind(minimum_height=self.setter('height'))
        self.src_toolbar=MDBoxLayout(size_hint=(1, None), spacing=dp(10))
        self.dest_toolbar=MDBoxLayout(size_hint=(1, None), spacing=dp(10))
        self.src_playsound=MDIconButton(icon="volume-high", theme_icon_color="Custom", icon_color=primarycolor, pos_hint={"right": 1, "center_y": 0.5}, size_hint=(None, None), size=(dp(20), dp(20)))
        self.src_copy=MDIconButton(icon="content-copy", theme_icon_color="Custom", icon_color=primarycolor, pos_hint={"right": 1, "center_y": 0.5}, size_hint=(None, None), size=(dp(20), dp(20)))
        self.dest_copy=MDIconButton(icon="content-copy", theme_icon_color="Custom", icon_color=primarycolor, pos_hint={"right": 1, "center_y": 0.5}, size_hint=(None, None), size=(dp(20), dp(20)))
        self.src_box=MDCard(orientation="vertical", size_hint=(1, 1), padding=[dp(10), dp(10), dp(10), dp(10)], md_bg_color=boxbg)
        self.src_text=MDTextField(hint_text="Nhập văn bản", mode="round", hint_text_color=[0.75-i for i in primarycolor], hint_text_color_focus=boxbg, line_color_normal=boxbg, line_color_focus=boxbg, text_color_focus=primarycolor, pos_hint={"center_x": 0.5, "center_y": 0.5}, multiline=True, fill_color_normal=boxbg)
        self.src=MDLabel(text="Anh", font_style="H6", size_hint=(1, None), theme_text_color="Custom", text_color=primarycolor, pos_hint={"center_y": 0.5})
        self.src_scroll=ScrollView(size_hint=(1, 1), do_scroll_x=False)
        self.src_edit=MDIconButton(icon="pencil", theme_icon_color="Custom", icon_color=primarycolor, pos_hint={"right": 1})
        self.dest_box=MDCard(orientation="vertical", size_hint=(1, 1), padding=[dp(10), dp(10), dp(10), dp(10)], md_bg_color=boxbg)
        self.dest=MDLabel(text="Việt", font_style="H6", size_hint=(1, None), theme_text_color="Custom", text_color=primarycolor, pos_hint={"center_y": 0.5})
        self.dest_text=MDTextField(hint_text="Kết quả sẽ hiển thị ở đây", mode="round", hint_text_color=[0.75-i for i in primarycolor], hint_text_color_focus=boxbg, line_color_normal=boxbg, line_color_focus=boxbg, text_color_normal=primarycolor, pos_hint={"center_x": 0.5, "center_y": 0.5}, multiline=True, fill_color_normal=boxbg)
        self.dest_text.is_focusable=False
        self.dest_scroll=ScrollView(size_hint=(1, 1), do_scroll_x=False)
        self.src_toolbar.bind(minimum_height=self.src_toolbar.setter('height'))
        self.dest_toolbar.bind(minimum_height=self.dest_toolbar.setter('height'))
        self.src_copy.bind(on_release=lambda instance: self.copy(instance, self.src_text.text))
        self.dest_copy.bind(on_release=lambda instance: self.copy(instance, self.dest_text.text))
        self.src_playsound.bind(on_release=lambda instance: self.pronounce(instance, self.src_text.text))
        self.dest.bind(texture_size=self.dest.setter('text_size'))
        self.dest.bind(texture_size=self.dest.setter('size'))
        self.src.bind(texture_size=self.src.setter('text_size'))
        self.src.bind(texture_size=self.src.setter('size')) 
        self.src_edit.bind(on_release=self.focus_src)
        self.src_text.bind(text=self.update_dest_text)
        self.src_text.bind(cursor=self.update_scroll)
        self.src_toolbar.add_widget(self.src)
        self.src_toolbar.add_widget(self.src_playsound)
        self.src_toolbar.add_widget(self.src_copy)
        self.add_widget(self.src_toolbar)
        self.add_widget(self.src_box)
        self.src_box.add_widget(self.src_scroll)
        self.src_box.add_widget(self.src_edit)
        self.src_scroll.add_widget(self.src_text)
        self.dest_toolbar.add_widget(self.dest)
        self.dest_toolbar.add_widget(self.dest_copy)
        self.add_widget(self.dest_toolbar)
        self.dest_box.add_widget(self.dest_scroll)
        self.dest_scroll.add_widget(self.dest_text)
        self.add_widget(self.dest_box)
        
    def copy(self, instance, text):
        pyperclip.copy(text)
        MDSnackbar(MDLabel(text="Đã sao chép nội dung", theme_text_color="Custom", text_color=primarycolor), md_bg_color=menubg, y=dp(10),  size_hint_x=.85, pos_hint={"center_x": 0.5}, radius=[dp(25), dp(25), dp(25), dp(25)]).open()
        
    def pronounce(self, instance, text):
        instance.disabled=True
        threading.Thread(target=self.run, args=[instance, text]).start()
        
    def run(self, instance, text):
        if engine:
            engine.say(text)
            engine.runAndWait()
            engine.stop()
        else:
            try: tts = gTTS(text)
            except:Clock.schedule_once(self.parent.parent.parent.parent.no_internet_alert.open)
            else:
                file_name="temp.wav"
                tts.save(file_name)
                sound = SoundLoader.load(file_name)
                if sound:
                    sound.play()
                    if os.path.exists(file_name):
                        os.remove(file_name)

        Clock.schedule_once(partial(self.eb, w=instance))

    def eb(self, instance, w):
        w.disabled=False
        
    def focus_src(self, instance):
        self.src_text.focus=True

    def update_scroll(self, instance, value):
        if self.src_text.height>=self.src_scroll.height and self.src_scroll.height!=0: Animation(scroll_y=1-(value[1]+1)/len(self.src_text._lines)).start(self.src_scroll)
        
    def update_dest_text(self, instance, value):
        if self.translate_thread:
            self.translate_event.set()
            self.translate_thread.join()
        if self.src_text.text.strip() != "":
            self.translate_event.clear()
            self.translate_thread = threading.Thread(target=self.delay_translate)
            self.translate_thread.start()
        else: self.dest_text.text=""

    def delay_translate(self):
        if not self.translate_event.wait(1): self.translate()

    def translate(self):
        if check_connection():
            try:
                translated_text = translator.translate(self.src_text.text, src='en', dest='vi').text
                Clock.schedule_once(lambda dt: self.update_dest_text_ui(translated_text))
            except: Clock.schedule_once(lambda dt: self.parent.parent.parent.parent.alert.open())
        else: Clock.schedule_once(lambda dt: self.parent.parent.parent.parent.no_internet_alert.open())

    def update_dest_text_ui(self, translated_text):
        self.dest_text.text=translated_text
        fade_in_vertical(self.dest_text)
