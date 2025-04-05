from ui import *

class InputFeature(MDBoxLayout):
    def __init__(self, **kwargs):
        super(InputFeature, self).__init__(**kwargs)
        self.got_check=None
        self.orientation="vertical"
        self.size_hint=(1, None)
        self.padding=[dp(10), dp(10), dp(10), dp(10)]
        self.spacing=dp(10)
        self.bind(minimum_height=self.setter('height'))
        self.add_widget(self.choose_box("Tìm kiếm tức thì", "search"))
        self.add_widget(self.choose_box("Gợi ý sửa chính tả", "suggest"))
        
    def choose_box(self, text, value):
        container=MDBoxLayout(size_hint=(1, None), height=dp(50), pos_hint={"center_x":0.5})
        title=MDLabel(text=text, theme_text_color="Custom", text_color=primarycolor)
        check_box=MDIconButton(icon="circle-outline", size=(dp(48), dp(48)), size_hint=(None, None), theme_icon_color="Custom", icon_color=btn)
        check_box.value=value
        container.add_widget(check_box)
        container.add_widget(title)
        check_box.bind(on_release=self.on_active)
        if settings['input feature']==value:
            self.got_check=check_box
            check_box.icon="check-circle"
        
        return container
    
    def on_active(self, instance):
        self.got_check.icon="circle-outline"
        instance.icon="check-circle"
        self.got_check=instance
        settings['input feature']=instance.value