from ui import *
from ui.setting.widget.change_palette import change_palette
from ui.setting.widget.change_fonts import change_fonts

update_thread=None

class setting(MDBoxLayout):
    def __init__(self, **kwargs):
        super(setting, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [10*scale, 10*scale, 10*scale, 10*scale]
        self.spacing=20*scale
        self.md_bg_color=bg
        
        self.overlay=MDCard(padding=[10*scale, 10*scale, 10*scale, 10*scale], size_hint=(1, 1), orientation='vertical', md_bg_color=bg)
        self.overlay.bind(on_touch=self.touch_ignore)
        self.overlay.cancel_button=MDFillRoundFlatButton(text="Huỷ", pos_hint={"center_x": 0.5, "center_y": 0.5}, theme_text_color="Custom", text_color=secondarycolor, md_bg_color=btn, on_press=self.cancel_update)
        self.overlay.add_widget(Image(source=settings["banner"], size_hint=(0.9, None), pos_hint={'center_x': 0.5, "center_y": 0.5}, height=50*scale))
        self.overlay.add_widget(MDLabel(text="Đang cập nhật...", font_style="H6", halign="center", valign="middle", pos_hint={"center_x": 0.5, "center_y": 0.5}, theme_text_color="Custom", text_color=primarycolor))
        self.overlay.add_widget(self.overlay.cancel_button)

        self.success=MDDialog(
            title="Cập nhật thành công.",
            type="alert",
            text="Khởi động lại để áp dụng dữ liệu mới.",
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
        self.success.buttons[1].bind(on_release=self.success.dismiss)

        self.failed=MDDialog(
            title="Cập nhật thất bại",
            type="alert",
            buttons=[
                MDFillRoundFlatButton(
                    text="Đóng",
                    md_bg_color=btn,
                    theme_text_color="Custom",
                    text_color=secondarycolor
                )
            ],
            md_bg_color=boxbg
        )
        self.failed.buttons[0].bind(on_release=self.failed.dismiss)

        self.search_thread=None
        self.touch_count=0
        self.timer = None
        self.back_button=MDIconButton(icon="arrow-left", size_hint=(None, None), pos_hint={"left": 0})
        self.back_button.bind(on_press=self.back)
        self.scrollview=ScrollView(size_hint=(1,1), do_scroll_x=False)
        self.personalize=MDBoxLayout(orientation="vertical", size_hint=(1,None), pos_hint={"center_x": 0.5}, spacing=20*scale)
        self.personalize.bind(minimum_height=self.personalize.setter('height'))
        self.scrollview.add_widget(self.personalize)
        self.changecolor=MDLabel(text="Cá nhân hóa với bảng màu", font_style="H6", halign="left", size_hint=(1,None), height=30*scale, pos_hint={"center_x":0.5}, theme_text_color="Custom", text_color=primarycolor)
        self.color_palette_scroll=change_palette()
        self.change_fonts=MDLabel(text="Fonts", font_style="H6", halign="left", size_hint=(1,None), height=30*scale, pos_hint={"center_x":0.5}, theme_text_color="Custom", text_color=primarycolor)
        self.font_scroll=change_fonts()
        self.info=MDFillRoundFlatButton(text=f"Phiên bản: SOD {version}\nNgày phát hành: Unknown    UID: {settings['uid']}", font_style="Caption", halign="center", size_hint=(0.75,None), height=35*scale, pos_hint={"center_x": 0.5}, theme_text_color="Custom", text_color=primarycolor, md_bg_color=bg)
        self.info.bind(on_release=self.on_touch)

        '''self.notification=MDLabel(text="Bạn không thể thay đổi bất cứ cài đặt nào của ứng dụng trong phiên bản này. Vui lòng chờ phiên bản cập nhật tiếp theo.", font_style="H6", halign="center", size_hint=(0.75,1), pos_hint={"center_x": 0.5})
        self.add_widget(self.notification)'''

        self.add_widget(self.back_button)
        self.add_widget(self.scrollview)
        self.personalize.add_widget(self.changecolor)
        self.personalize.add_widget(self.color_palette_scroll)
        self.personalize.add_widget(self.change_fonts)
        self.personalize.add_widget(self.font_scroll)
        self.add_widget(self.info)

    def back(self, instance):
        sm.transition.direction = "right"
        sm.current = 'first'

    def on_touch(self, instance):
        self.cre=MDLabel(text=f"""Chào mừng bạn đến với {settings["title"]}!

Là nhà phát triển chính của {settings["title"]}, tôi muốn dành một chút thời gian để cảm ơn bạn đã sử dụng phần mềm của tôi.

{settings["title"]} được xây dựng bằng ngôn ngữ lập trình Python và sử dụng thư viện giao diện KivyMD. Tôi đã dành rất nhiều thời gian và công sức để tạo ra một sản phẩm mà tôi hy vọng sẽ hữu ích cho bạn.

Tôi rất biết ơn sự hỗ trợ và phản hồi của bạn. Những ý kiến đóng góp của bạn giúp tôi cải thiện {settings["title"]} và đảm bảo rằng nó đáp ứng nhu cầu của người dùng.

Nếu bạn có bất kỳ câu hỏi hoặc yêu cầu nào, đừng ngần ngại liên hệ với tôi qua email. Tôi luôn sẵn lòng giúp đỡ và mong muốn nghe ý kiến từ bạn.

Cảm ơn bạn đã sử dụng {settings["title"]}!

Trân trọng,
Nhật
                """,
                  font_style="Body2",
                  size_hint=(1,None),
                  height=25*scale,
                  pos_hint={"center_x": 0.5},
                  theme_text_color="Custom",
                  text_color=primarycolor)
        self.cre.bind(texture_size=self.cre.setter('text_size'))
        self.cre.bind(texture_size=self.cre.setter('size'))
        self.temp_scroll_box=ScrollView(size_hint=(1, 1), pos_hint={"center_x": 0.5}, do_scroll_x=False)
        self.temp_scroll_box.add_widget(self.cre)
        self.container=MDCard(orientation="vertical", spacing=20*scale, size_hint=(1,None), height=200*scale, padding=[10*scale, 10*scale, 10*scale, 10*scale])
        self.container.radius=[i*scale for i in self.container.radius]
        self.container.add_widget(self.temp_scroll_box)
        self.credit=MDDialog(
        title=f"Thư cảm ơn từ Nhà phát triển {settings['title']}",
        type="custom",
        content_cls=self.container,
        buttons=[
            MDFillRoundFlatButton(
                text="Cập nhật dữ liệu",
                md_bg_color=btn,
                theme_text_color="Custom",
                text_color=secondarycolor
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
        self.credit.buttons[0].bind(on_release=self.update_trigger)
        self.credit.buttons[1].bind(on_release=self.credit.dismiss)
        self.credit.open()
        
    def update_trigger(self, instance):
        global update_thread
        self.credit.dismiss()
        self.screen=sm.get_screen('second')
        self.screen.add_widget(self.overlay)
        update_thread=threading.Timer(1, self.update_)
        update_thread.start()
        
    def touch_ignore():
        pass

    def cancel_update(self, instance):
        global update_thread
        sm.get_screen('second').remove_widget(self.overlay)
        update_thread.cancel()
    
    def update_(self):
        self.overlay.cancel_button.disabled=True
        try:
            if check_connection():
                download_file("Whoop", "Whoop/func/data/tu_dien_nguon.txt", "func/data/tu_dien_nguon.txt")
                download_file("Whoop", "Whoop/func/data/word.txt", "func/data/word.txt")
                download_file("Whoop", "Whoop/func/data/grammar.txt", "func/data/grammar.txt")
        except:
            Clock.schedule_once(self.failed_)
        else:
            Clock.schedule_once(self.success_)
            
    def success_(self, instance):
        self.overlay.cancel_button.disabled=False
        self.screen.remove_widget(self.overlay)
        self.success.open()
        
    def failed_(self, instance):
        self.overlay.cancel_button.disabled=False
        self.screen.remove_widget(self.overlay)
        self.failed.open()
