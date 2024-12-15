from ui import *
import ui

class change_fonts(ScrollView):
    def __init__(self, **kwargs):
        super(change_fonts, self).__init__(**kwargs)
        self.icon=MDIconButton(icon="check-circle", theme_icon_color="Custom", icon_color=primarycolor, size_hint=(None, None), pos_hint={"center_x": 0.5})
        self.got_font_check=None
        self.do_scroll_y=False
        self.size_hint=(1, None)
        self.height=dp(50)
        self.font_list=MDBoxLayout(size_hint=(None, 1), pos_hint={"center_x": 0.5}, spacing=dp(20), padding=[dp(10), dp(10), dp(10), dp(10)])
        self.font_list.height=dp(self.font_list.height)
        self.font_list.bind(minimum_width=self.font_list.setter('width'))
        self.add_widget(self.font_list)
        for i in fonts_name:
            self.font_list.add_widget(self.create_preview(i))

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

    def create_preview(self, i):
        self.font=MDFillRoundFlatIconButton(text=i, theme_icon_color='Custom', md_bg_color=btn, theme_text_color="Custom", text_color=secondarycolor, font_name=f"func/setting/fonts/{i}.ttf", font_size=dp(17))
        if i==settings["fonts"]:
            self.font.icon='check-circle'
            self.font.icon_color=secondarycolor
            self.got_font_check=self.font
        self.font.bind(on_press=lambda instance: self.change_font(instance, i))

        return self.font

    def change_font(self, instance, i):
        self.got_font_check.icon=''
        self.got_font_check=instance
        instance.icon='check-circle'
        instance.icon_color=secondarycolor
        self.scroll_to(self.got_font_check)
        ui.settings["fonts"]=i
        self.dialog.open()