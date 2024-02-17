from ui.init import *
from ui.main import Main
from ui.setting import Setting

class FirstScreen(Screen):
    def __init__(self, **kwargs):
        super(FirstScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [10, 10, 10, 10]
        self.spacing = 20
        
        layout = Main()
        self.add_widget(layout)

class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super(SecondScreen, self).__init__(**kwargs)
        setting_layout = Setting()
        self.add_widget(setting_layout)

    def __getattr__(self, name):
        if name == 'second':
            self.layout = Main()
            self.add_widget(self.layout)
            return self.layout
        return super().__getattr__(name)

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
    config()
    MyApp().run()
    set_new_config()