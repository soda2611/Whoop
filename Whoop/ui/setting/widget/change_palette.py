from ui import *
import ui

class change_palette(ScrollView):
    def __init__(self, **kwargs):
        super(change_palette, self).__init__(**kwargs)
        self.icon=MDIconButton(icon="check-circle", theme_icon_color="Custom", icon_color=primarycolor, size_hint=(None, None), pos_hint={"center_x": 0.5})
        self.got_check=None
        self.do_scroll_y=False
        self.size_hint=(1, None)
        self.height=dp(300)
        self.color_palette_list=MDBoxLayout(size_hint=(None, 1), pos_hint={"center_x": 0.5}, spacing=dp(20), padding=[dp(10), dp(10), dp(10), dp(10)])
        self.color_palette_list.bind(minimum_width=self.color_palette_list.setter('width'))
        self.add_widget(self.color_palette_list)
        for i in colors:
            self.color_palette_list.add_widget(self.create_palette(i))

        self.dialog = MDDialog(
            title="Cài đặt liên quan đến cá nhân hóa sẽ được áp dụng khi bạn khởi động lại ứng dụng",
            type="alert",
            buttons=[
                MDFillRoundFlatButton(
                    text="Khởi động lại",
                    md_bg_color=btn,
                    theme_text_color="Custom",
                    text_color=secondarycolor,
                    on_press=restart
                ),
                MDFillRoundFlatButton(
                    text="Đóng",
                    md_bg_color=btn,
                    theme_text_color="Custom",
                    text_color=secondarycolor
                )
            ],
            md_bg_color=boxbg
        )
        self.dialog.buttons[1].bind(on_release=self.dialog.dismiss)

    def create_palette(self, i):
        self.color=MDCard(md_bg_color=(1,1,1,1), orientation="vertical", size_hint=(None, None), width=dp(50), height=dp(200), pos_hint={"center_x": 0.5}, padding=[dp(10), dp(10), dp(10), dp(10)], ripple_behavior=True)
        self.color.radius=[dp(k) for k in self.color.radius]
        theme=[]
        for j in i:
            theme.append([int(j[0])/255,int(j[1])/255,int(j[2])/255, 1])
        for j in i[:4]:
            self.color1=MDBoxLayout(md_bg_color=(int(j[0])/255,int(j[1])/255,int(j[2])/255, 1),size_hint=(1,0.25), pos_hint={"center_x":0.5})
            self.color.add_widget(self.color1)
        if [[str(int(i*255)) for i in bg[:-1]], [str(int(i*255)) for i in boxbg[:-1]], [str(int(i*255)) for i in menubg[:-1]], [str(int(i*255)) for i in btn[:-1]]]==i[:4]:
            self.color.height=dp(250)
            self.color.add_widget(self.icon)
            self.got_check=self.color
        self.color.bind(on_press=lambda instance: self.change_color_theme(instance, theme[0], theme[1], theme[2], theme[3], theme[4], theme[5]))

        return self.color

    def change_color_theme(self, instance, new_bg, new_boxbg, new_menubg, new_btn, new_primarycolor, new_secondarycolor):
        try: self.got_check.remove_widget(self.icon)
        except: pass
        self.got_check.height=dp(200)
        self.got_check=instance
        instance.height=dp(250)
        instance.add_widget(self.icon)
        self.scroll_to(self.got_check)
        ui.settings["current palette"]="; ".join([", ".join([str(int(i*255)) for i in new_bg][:-1]),", ".join([str(int(i*255)) for i in new_boxbg][:-1]),", ".join([str(int(i*255)) for i in new_menubg][:-1]),", ".join([str(int(i*255)) for i in new_btn][:-1]), ", ".join([str(int(i*255)) for i in new_primarycolor][:-1]), ", ".join([str(int(i*255)) for i in new_secondarycolor][:-1])])
        self.dialog.open()