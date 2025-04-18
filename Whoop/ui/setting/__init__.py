from ui import *
from ui.setting.widget.change_palette import change_palette
from ui.setting.widget.change_fonts import change_fonts
from ui.setting.widget.update_dialog import update_dialog
from ui.setting.widget.input_feature import InputFeature

update_thread=None

class setting(MDBoxLayout):
    def __init__(self, **kwargs):
        super(setting, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [dp(10), dp(10), dp(10), dp(10)]
        self.spacing=dp(20)

        self.no_internet_alert=self.alert=MDDialog(
            title="Không có kết nối internet",
            type="alert",
            md_bg_color=boxbg
        )

        self.overlay=MDCard(padding=[dp(10), dp(10), dp(10), dp(10)], size_hint=(1, 1), orientation='vertical', md_bg_color=bg, radius=[0, 0, 0, 0])
        self.overlay.bind(on_touch=self.touch_ignore)
        self.overlay.cancel_button=MDFillRoundFlatButton(text="Huỷ", pos_hint={"center_x": 0.5, "center_y": 0.5}, theme_text_color="Custom", text_color=secondarycolor, md_bg_color=btn, on_press=self.cancel_update)
        self.overlay.add_widget(Image(source=settings["banner"], size_hint=(0.9, None), pos_hint={'center_x': 0.5, "center_y": 0.5}, height=dp(50)))
        self.overlay.add_widget(Label(text=f"Đang cập nhật...\n[font=func/setting/fonts/arial][size={int(dp(12))}]Điều này có thể kéo dài nhiều phút[/size][/font]", markup=True, font_name=f"func/setting/fonts/{settings['fonts']}.ttf", font_size=dp(20), halign="center", valign="middle", pos_hint={"center_x": 0.5, "center_y": 0.5}, color=primarycolor))
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
        self.back_button=MDIconButton(icon="arrow-left", theme_icon_color="Custom", icon_color=primarycolor, size_hint=(None, None), pos_hint={"left": 0, "center_y": 0.5})
        self.back_button.bind(on_press=self.back)
        self.scrollview=ScrollView(size_hint=(1,1), do_scroll_x=False)
        self.input_feature=MDLabel(text="Thiết lập hành vi thanh tìm kiếm", font_style="H6", halign="left", size_hint=(1,None), height=dp(30), pos_hint={"center_x":0.5}, theme_text_color="Custom", text_color=primarycolor)
        self.input_feature.choose=InputFeature()
        self.personalize=MDBoxLayout(orientation="vertical", size_hint=(1,None), pos_hint={"center_x": 0.5}, spacing=dp(20))
        self.personalize.bind(minimum_height=self.personalize.setter('height'))
        self.scrollview.add_widget(self.personalize)
        self.changecolor=MDLabel(text="Palettes", font_style="H6", halign="left", size_hint=(1,None), height=dp(30), pos_hint={"center_x":0.5}, theme_text_color="Custom", text_color=primarycolor)
        self.color_palette_scroll=change_palette()
        self.change_fonts=MDLabel(text="Fonts", font_style="H6", halign="left", size_hint=(1,None), height=dp(30), pos_hint={"center_x":0.5}, theme_text_color="Custom", text_color=primarycolor)
        self.font_scroll=change_fonts()
        self.info=MDFillRoundFlatButton(text=f"Phiên bản: {version}\nNgày phát hành: {settings['released date']}    UID: {settings['uid']}", font_style="Caption", halign="center", size_hint=(0.75,None), height=dp(35), pos_hint={"center_x": 0.5}, theme_text_color="Custom", text_color=primarycolor, md_bg_color=bg)
        self.info.bind(on_release=self.update_dialog_open)

        '''self.notification=MDLabel(text="Bạn không thể thay đổi bất cứ cài đặt nào của ứng dụng trong phiên bản này. Vui lòng chờ phiên bản cập nhật tiếp theo.", font_style="H6", halign="center", size_hint=(0.75,1), pos_hint={"center_x": 0.5})
        self.add_widget(self.notification)'''

        self.add_widget(self.back_button)
        self.add_widget(self.scrollview)
        self.personalize.add_widget(self.input_feature)
        self.personalize.add_widget(self.input_feature.choose)
        self.personalize.add_widget(self.changecolor)
        self.personalize.add_widget(self.color_palette_scroll)
        self.personalize.add_widget(self.change_fonts)
        self.personalize.add_widget(self.font_scroll)
        self.add_widget(self.info)
        
    def on_choose(self, instance, *args):
        print(instance.text)
        if instance.text=="Tìm kiếm từ":
            settings["input feature"]="search"
        else:
            settings["input feature"]="suggest"

    def back(self, instance):
        sm.current = 'first'
        
    def update_dialog_open(self, instance):
        self.screen=sm.get_screen('second')
        self.screen.update_dialog.official.bind(on_press=lambda instance: self.update_trigger(instance, "official"))
        self.screen.update_dialog.early_access.bind(on_press=lambda instance: self.update_trigger(instance, "early-access"))
        self.screen.update_dialog.open()

    def update_trigger(self, instance, _type_):
        global update_thread
        try: self.screen.add_widget(self.overlay)
        except: pass
        else:
            update_thread=threading.Timer(2, self.update_, args=[_type_])
            update_thread.start()

    def touch_ignore():
        pass

    def cancel_update(self, instance):
        global update_thread
        update_thread.cancel()
        self.screen.remove_widget(self.overlay)

    def update_(self, _type_=None, _dialog_=True):
        print(_type_)
        if _dialog_: self.overlay.cancel_button.disabled=True
        try:
            if check_connection():
                if _type_=="early-access":
                    os.system("mkdir temp_data")
                    download_file('whoop_database', 'users', 'temp_data')
                    download_file('Whoop', 'Whoop/func/data/tu_dien_nguon.txt', 'temp_tu_dien_nguon.txt')
                    download_file('Whoop', 'Whoop/func/data/source.txt', 'temp_source.txt')
                    with open('func/data/tu_dien_nguon.txt', encoding='utf-8') as fi: dict_=eval(fi.read())
                    with open('temp_source.txt', encoding='utf-8') as fi: source=eval(fi.read())
                    with open('temp_tu_dien_nguon.txt', encoding='utf-8') as fi: _dict_=eval(fi.read())
                    with open('func/data/source.txt', encoding='utf-8') as fi: _source_=eval(fi.read())
                    for root, dirs, files in os.walk('temp_data'):
                            for file in files:
                                if file.endswith(".txt"):
                                    with open(f'temp_data/{file}', encoding="utf-8") as fi:
                                        data=fi.read()
                                        dict_.update(eval(data))
                                        _dict_.update(eval(data))
                                        dict_ = {k: v for k, v in dict_.items() if v!="Không tìm thấy từ"}
                                        _dict_ = {k: v for k, v in _dict_.items() if v!="Không tìm thấy từ"}
                                os.remove(f'temp_data/{file}')        
                    with open('func/data/tu_dien_nguon.txt', "w", encoding='utf-8') as fo: fo.write(json.dumps(dict_, ensure_ascii=False, indent=4))
                    with open('temp_tu_dien_nguon.txt', "w", encoding='utf-8') as fo: fo.write(json.dumps(_dict_, ensure_ascii=False, indent=4))
                    with open('func/data/source.txt', "w", encoding='utf-8') as fo: fo.write(str(list(set(source+_source_))))
                    upload_file('Whoop', 'Whoop/func/data/tu_dien_nguon.txt', 'temp_tu_dien_nguon.txt')
                    os.removedirs('temp_data')
                elif _type_=="official":
                    download_file('Whoop', 'Whoop/func/data/tu_dien_nguon.txt', 'temp_tu_dien_nguon.txt')
                    download_file('Whoop', 'Whoop/func/data/source.txt', 'temp_source.txt')
                    with open('func/data/tu_dien_nguon.txt', encoding='utf-8') as fi: dict_=eval(fi.read())
                    with open('temp_tu_dien_nguon.txt', encoding='utf-8') as fi: _dict_=eval(fi.read())
                    with open('temp_source.txt', encoding='utf-8') as fi: source=eval(fi.read())
                    with open('func/data/source.txt', encoding='utf-8') as fi: _source_=eval(fi.read())
                    with open('func/data/source.txt', "w", encoding='utf-8') as fo: fo.write(str(list(set(source+_source_))))
                    dict_.update(_dict_)
                    with open('func/data/tu_dien_nguon.txt', "w", encoding='utf-8') as fo: fo.write(json.dumps(dict_, ensure_ascii=False, indent=4))
                    download_file("Whoop", "Whoop/func/data/word.txt", "func/data/word.txt")
                os.remove('temp_tu_dien_nguon.txt')
                os.remove('temp_source.txt')
                if _dialog_: Clock.schedule_once(self.success_)
            else:
                if _dialog_: Clock.schedule_once(self.no_internet)
        except Exception as ex:
            print(ex)
            if _dialog_: Clock.schedule_once(self.failed_)

    def success_(self, instance):
        self.overlay.cancel_button.disabled=False
        self.screen.remove_widget(self.overlay)
        self.screen.update_dialog.dismiss()
        self.success.open()

    def failed_(self, instance):
        self.overlay.cancel_button.disabled=False
        self.screen.remove_widget(self.overlay)
        self.screen.update_dialog.dismiss()
        self.failed.open()
        
    def no_internet(self, instance):
        self.overlay.cancel_button.disabled=False
        self.screen.remove_widget(self.overlay)
        self.screen.update_dialog.dismiss()
        self.no_internet_alert.open()
