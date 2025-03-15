from ui import *

conversation_history = [
    {
        "role": "user",
        "parts": [
            {"text": "You play a role of an friendly English teacher during this conversation (just speak English). From now, you're called 'Whoop AI' and powered by Gemini"}
        ]
    }
]

class chat(MDBoxLayout):
    def __init__(self, **kwargs):
        super(chat, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [dp(20), dp(10), dp(20), dp(35)]
        self.spacing = dp(10)
        self.message=""
        
        self.top_bar=MDFloatLayout(size_hint=(1, None), height=dp(70))
        
        self.back_button=MDIconButton(icon="arrow-left", theme_icon_color="Custom", icon_color=primarycolor, size_hint=(None, None), pos_hint={"left": 0, "center_y": 0.5})
        self.back_button.bind(on_press=self.back)
        self.label = Image(source="func/setting/img/whoop_ai.png", size_hint=(1, None), pos_hint={'center_x': 0.5, "center_y": 0.5}, height=dp(50))
        self.top_bar.add_widget(self.label)
        self.top_bar.add_widget(self.back_button)
        
        self.text_input = MDRelativeLayout(size_hint=(1, None), height=dp(50), pos_hint={'center_x': 0.5, "center_y": 0.5})
        self.text_input.input = MDTextField(
            icon_left="message",
            icon_left_color_focus=btn,
            hint_text="What can I help you?",
            line_color_normal=boxbg,
            line_color_focus=menubg,
            hint_text_color=[0.75 - i for i in primarycolor],
            hint_text_color_focus=primarycolor,
            text_color_focus=primarycolor,
            fill_color_normal=boxbg,
            mode="round",
            size_hint=(1, None),
            pos_hint={'center_y': 0.5},
            height=dp(30),
            multiline=False,
            on_text_validate=self.send_message
        )
        
        self.text_input.button = MDIconButton(
            icon='send-variant',
            disabled=True,
            theme_icon_color="Custom",
            icon_color=btn,
            size_hint=(None, None),
            pos_hint={"right": 1, "bottom": 0},
            on_release=self.send_message
        )
        
        self.message_box = MDBoxLayout(orientation="vertical", size_hint=(1, None), padding=[dp(10), dp(10), dp(10), dp(10)], pos_hint={'center_y': 0.5})
        self.message_scroll = ScrollView(do_scroll_x=False, size_hint=(1, 1))
        self.message_box.bind(minimum_height=self.message_box.setter('height'))
        
        self.add_widget(self.top_bar)
        self.add_widget(self.message_scroll)
        self.message_scroll.add_widget(self.message_box)
        self.text_input.add_widget(self.text_input.input)
        self.text_input.add_widget(self.text_input.button)
        self.text_input.input.bind(text=self.on_text)
        self.add_widget(self.text_input)
        
    def on_text(self, instance, value):
        self.text_input.button.disabled=False if value.strip()!="" else True
        
    def send_message(self, instance):
        user_message = MDLabel(
            text=self.text_input.input.text,
            halign="left",
            theme_text_color="Custom",
            text_color=primarycolor,
            font_style="Body1",
            size_hint=(1, None),
            markup=True,
        )
        user_message.bind(texture_size=user_message.setter('texture_size'))
        user_message.bind(texture_size=user_message.setter('size'))
        
        user_content = MDCard(
            radius=[dp(10), dp(10), dp(10), dp(10)], 
            size_hint=(1, None), 
            padding=[dp(10), dp(10), dp(10), dp(10)],
            spacing=dp(20)
        )
        user_content.bind(minimum_height=user_content.setter('height'))
        user_content.add_widget(MDIcon(icon="account", pos_hint={"top": 1}))
        user_content.add_widget(user_message)
        self.message_box.add_widget(user_content)
        fade_in(user_content, on_complete=lambda instance: threading.Thread(target=self.get_respond).start())
        if self.message_box.height>self.message_scroll.height and self.message_scroll.height!=0: Animation(scroll_y=0, transition="out_quad").start(self.message_scroll)
        self.message=self.text_input.input.text
        self.text_input.input.text = ""
        
    def get_respond(self):
        global respond, conversation_history
        respond, conversation_history = whoop_ai(self.message, conversation_history)
        respond = process_readme(respond)
        Clock.schedule_once(self.show_message)
        
    def show_message(self, instance):
        bot_message = MDLabel(
            text=respond,
            halign="left",
            theme_text_color="Custom",
            text_color=primarycolor,
            font_style="Body1",
            size_hint=(1, None),
            markup=True,
        )
        bot_message.bind(texture_size=bot_message.setter('texture_size'))
        bot_message.bind(texture_size=bot_message.setter('size'))
        
        content = MDCard(
            radius=[dp(10), dp(10), dp(10), dp(10)], 
            size_hint=(1, None), 
            padding=[dp(10), dp(10), dp(10), dp(10)],
            spacing=dp(20)
        )
        content.bind(minimum_height=content.setter('height'))
        content.add_widget(MDIcon(icon="creation", pos_hint={"top": 1}))
        content.add_widget(bot_message)
        self.message_box.add_widget(content)
        fade_in(content)
        if self.message_box.height>self.message_scroll.height and self.message_scroll.height!=0: Animation(scroll_y=0, transition="out_quad").start(self.message_scroll)
        
    def back(self, instance):
        sm.current = 'first'
