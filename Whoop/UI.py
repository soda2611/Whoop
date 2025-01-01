from ui import *
from ui.home import home
from ui.setting import setting, update_dialog
import kivy

class FirstScreen(MDScreen):
    def __init__(self, **kwargs):
        super(FirstScreen, self).__init__(**kwargs)
        layout = home()
        self.add_widget(FitImage(source=settings["pattern"], pos_hint={"center_x": 0.5, "bottom": 0}, size_hint_y=None, height=dp(80)))
        self.add_widget(layout)
        self.md_bg_color=bg

class SecondScreen(MDScreen):
    def __init__(self, **kwargs):
        super(SecondScreen, self).__init__(**kwargs)
        self.setting_layout = setting()
        self.update_dialog=update_dialog()
        self.add_widget(self.setting_layout)
        self.add_widget(self.update_dialog)
        self.md_bg_color=bg

class MyApp(MDApp):
    def build(self):
        global firstscreen, secondscreen
        self.icon=settings["icon"]
        self.title=settings["title"]
        firstscreen=FirstScreen(name='first')
        secondscreen=SecondScreen(name='second')
        secondscreen.setting_layout.color_palette_scroll.scroll_to(secondscreen.setting_layout.color_palette_scroll.got_check)
        secondscreen.setting_layout.font_scroll.scroll_to(secondscreen.setting_layout.font_scroll.got_font_check)
        sm.add_widget(firstscreen)
        sm.add_widget(secondscreen)
        sm.transition.duration=0.5
        return sm

if __name__ == '__main__':
    MyApp().run()
    set_new_config()
