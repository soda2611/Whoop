from ui import *
from ui.home import home
from ui.setting import setting, update_dialog

class FirstScreen(Screen):
    def __init__(self, **kwargs):
        super(FirstScreen, self).__init__(**kwargs)
        layout = home()
        self.add_widget(layout)

class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super(SecondScreen, self).__init__(**kwargs)
        setting_layout = setting()
        self.update_dialog=update_dialog()
        self.add_widget(setting_layout)
        self.add_widget(self.update_dialog)

class MyApp(MDApp):
    def build(self):
        global firstscreen, secondscreen
        self.icon=settings["icon"]
        self.title=settings["title"]
        firstscreen=FirstScreen(name='first')
        secondscreen=SecondScreen(name='second')
        sm.add_widget(firstscreen)
        sm.add_widget(secondscreen)
        return sm

if __name__ == '__main__':
    MyApp().run()
    set_new_config()
