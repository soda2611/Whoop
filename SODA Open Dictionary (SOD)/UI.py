from ui.init import *
from ui.main import main
from ui.setting import setting

class FirstScreen(Screen):
    def __init__(self, **kwargs):
        super(FirstScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [10, 10, 10, 10]
        self.spacing = 20
        
        layout = main()
        self.add_widget(layout)

class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super(SecondScreen, self).__init__(**kwargs)
        setting_layout = setting()
        self.add_widget(setting_layout)

    def __getattr__(self, name):
        if name == 'second':
            self.layout = main()
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
    open("func/main_pid.txt", "w", encoding="utf-8").write(str(os.getpid()))
    subprocess.Popen(["pyw", "func/crash_handle.pyw"], start_new_session=True)
    MyApp().run()
    set_new_config()