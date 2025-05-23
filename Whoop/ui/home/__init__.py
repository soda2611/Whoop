from ui import *
from ui.home.widget.result_template import *
from ui.home.widget.add_data import add_data
from ui.home.widget.recent import *
from ui.home.widget.content_box import *
from ui.home.widget.fav_word_list import *
from ui.home.widget.suggest import *

current_page="home"
_temp_=[]
_back_=[]
_value_=True
_callback_=False
_key_=None
result={}
generated=[]
folders=OrderedDict({})

class home(MDBoxLayout, TouchBehavior):
    def __init__(self, **kwargs):
        super(home, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [dp(10), dp(10), dp(10), dp(35)]
        self.spacing = dp(25)

        self.text=""
        self.signal=False
        self.search_thread = None
        self.search_event = threading.Event()
        self.possible_word = []

        theme_font_styles.append('main')
        self.theme_cls.font_styles["main"] = ["main", 16, False, 0.15]

        self.alert=MDDialog(
            title="Lỗi trong khi dịch",
            type="alert",
            md_bg_color=boxbg
        )

        self.no_internet_alert=self.alert=MDDialog(
            title="Không có kết nối internet",
            type="alert",
            md_bg_color=boxbg
        )

        self.fav_container=MDTextField(hint_text="Tên danh mục", line_color_normal=boxbg, line_color_focus=menubg, hint_text_color=[0.75-i for i in primarycolor], hint_text_color_focus=primarycolor, text_color_focus=primarycolor, fill_color_normal=boxbg, mode="round", size_hint=(1, None), pos_hint={'center_x': 0.5}, height=dp(30), multiline=False)
        self.fav_container.bind(on_text_validate=self.add_fav)

        self.fav_dialog=MDDialog(
            title=f"Thêm danh mục yêu thích",
            type="custom",
            content_cls=self.fav_container,
            buttons=[
                MDFillRoundFlatButton(
                    text="Xác nhận",
                    md_bg_color=btn,
                    theme_text_color="Custom",
                    text_color=secondarycolor,
                    on_press=self.add_fav
                ),
                MDFillRoundFlatButton(
                    text="Huỷ",
                    md_bg_color=btn,
                    theme_text_color="Custom",
                    text_color=secondarycolor,
                )],
            md_bg_color=boxbg
        )
        self.fav_dialog.buttons[1].bind(on_press=self.fav_dialog.dismiss)

        self.label = Image(source=settings["banner"], size_hint=(0.9, None), pos_hint={'center_x': 0.5}, height=dp(55))

        self.resultlabel = MDLabel(text='', font_style="H6", halign='center', valign='middle', size_hint=(1, None), pos_hint={'center_x': 0.5, 'center_y': 0.5}, height=30)

        self.combine_box=MDBoxLayout(orientation='vertical', size_hint=(0.9, None), pos_hint={'center_x': 0.5, "center_y": 0.5}, spacing=dp(10))
        self.combine_box.suggest_box=MDBoxLayout(orientation='vertical', size_hint=(1, None), height=dp(0), pos_hint={'center_x': 0.5, "center_y": 0.5})
        self.combine_box.suggest_scroll=suggest([])
        self.text_input=MDRelativeLayout(size_hint=(1, None), height=dp(50), pos_hint={'center_x': 0.5, "center_y": 0.5})
        self.text_input.input=MDTextField(icon_left="magnify", icon_right="bruh", icon_left_color_focus=btn, hint_text="Nhập từ cần tìm", line_color_normal=boxbg, line_color_focus=menubg, hint_text_color=[0.75-i for i in primarycolor], hint_text_color_focus=primarycolor, text_color_focus=primarycolor, fill_color_normal=boxbg, mode="round", size_hint=(1, None), pos_hint={'center_y': 0.5}, height=dp(30), multiline=False, on_text_validate=lambda instance: self.search_button_pressed(instance, word_detector(spelling_checker_for_SOD(" ".join(self.text_input.input.text.lower().split())))))        
        self.text_input.left_icon=MDIconButton(icon='magnify', theme_icon_color="Custom", disabled_color=btn, disabled=True, size_hint=(None, None), pos_hint={"left": 0, "center_y":0.5})
        self.text_input.button=MDIconButton(icon='translate', theme_icon_color="Custom", icon_color=btn, size_hint=(None, None), pos_hint={"right": 1, "center_y":0.5}, on_release=self.translate)

        self.hib=MDIconButton(icon='close', theme_icon_color="Custom", icon_color=primarycolor, size_hint=(None, None), pos_hint={"center_x": 0.5, "center_y":0.5})
        self.hib.bind(on_press=self.on_double_tap)

        self.button = MDIconButton(icon='magnify', theme_icon_color="Custom", icon_color=secondarycolor, size_hint=(1, None), pos_hint={"center_x":0.5})

        self.homebutton = MDIconButton(icon='home', theme_icon_color="Custom", icon_color=secondarycolor, size_hint=(1, None), pos_hint={"x":0})

        self.menubutton = MDIconButton(icon='menu', theme_icon_color="Custom", icon_color=secondarycolor, size_hint=(1, None), pos_hint={"x":1})

        self.progress_box=MDBoxLayout(orientation='vertical', size_hint=(0.95,None), height=dp(5), pos_hint={"center_x":0.5})

        self.progress_bar = MDProgressBar(radius=[5,5,5,5], type="indeterminate", pos_hint={"center_x":0.5}, running_duration=0.75, catching_duration=0.5, color=btn, back_color=bg)

        self.one_box=MDBoxLayout(size_hint=(0.85, 0.25), pos_hint={'center_x': 0.5, 'center_y': 0.5}, spacing = 20)

        self.nav_bar=MDBoxLayout(size_hint=(1, None), height=dp(50))
        self.back_button=MDIconButton(icon="arrow-left", theme_icon_color="Custom", pos_hint={"center_y": 0.5}, icon_color=primarycolor, md_bg_color=(1,1,1,0), disabled=True, md_bg_color_disabled=(1,1,1,0), on_press=self.back)
        self.noname=MDCard(orientation='vertical',md_bg_color=bg, size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.noname.radius=[dp(i) for i in self.noname.radius]

        self.fav_nav_bar=MDBoxLayout(size_hint=(1, None), height=dp(50))
        self.fav_back_button=MDIconButton(icon="arrow-left", theme_icon_color="Custom", pos_hint={"center_y": 0.5}, icon_color=primarycolor, md_bg_color=(1,1,1,0), disabled=True, md_bg_color_disabled=(1,1,1,0), on_press=self.back)
        self.fav_label=MDLabel(text="Yêu thích", font_style="main", font_size=dp(20), halign='center', valign='middle', size_hint=(1, None), pos_hint={'center_x': 0.5, "center_y": 0.5}, theme_text_color="Custom", text_color=primarycolor)
        self.add_button=MDIconButton(icon="plus", theme_icon_color="Custom", icon_color=primarycolor, pos_hint={"x": 1, "center_y": 0.5})
        self.add_button.bind(on_press=self.fav_dialog.open)

        self.favlist=favwordlist()
        self.favlist.bind(choose_mode=self.on_choose_mode)
        if len(fav_list)>0:
            for i in fav_list:
                if len(fav_list[i])>0:
                    _data_=fav_list[i]
                    _folder_=folder(i, f"Có {len(fav_list[i])} từ vựng")
                    self.favlist.fav_scrollview_box.add_widget(_folder_)
                else:
                    _folder_=folder(i, f"Không có từ vựng")
                    self.favlist.fav_scrollview_box.add_widget(_folder_)
                _folder_.folder_len=len(fav_list[i])
                _folder_.bind(folder_len=self.on_folder_len)
                folders.update([(i, _folder_)])
                rename=MDIconButton(icon="rename", theme_icon_color="Custom", icon_color=primarycolor, pos_hint={"center_x": 0.5, "center_y": 0.5})
                rename.bind(on_press=self.renamefav)
                _folder_.add_widget(rename)
                _folder_.add_widget(MDIconButton(icon="delete", theme_icon_color="Custom", icon_color=primarycolor, pos_hint={"center_x": 0.5, "center_y": 0.5}, on_press=lambda instance: self.remove_fav(instance)))

                if not self.favlist.choose_mode and len(fav_list[i])>0:
                    _folder_.morebutton=MDIconButton(icon="chevron-right", theme_icon_color="Custom", icon_color=primarycolor, pos_hint={"center_x": 0.5, "center_y": 0.5})
                    _folder_.morebutton.bind(on_press=partial(self.show_fav_folder, folder=i))
                    _folder_.add_widget(_folder_.morebutton)
            self.favlist.container.add_widget(self.favlist.fav_scrollview)
        else:
            self.favlist.container.add_widget(self.favlist.label)

        self.scrollview = ScrollView(size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5}, on_scroll_stop=self.infinite_homepage)

        self.result_box=MDBoxLayout(orientation='vertical', size_hint=(1,None), spacing=dp(20), padding=[dp(10), dp(10), dp(10), dp(10)])
        self.result_box.bind(minimum_height=self.result_box.setter('height'))
        
        self.add_data_=add_data()

        self.homebox=MDBoxLayout(spacing=dp(20))
        self.scrollview.do_scroll_x=False
        self.homebox.orientation="vertical"
        self.homebox.size_hint_y=None
        self.homebox.bind(minimum_height=self.homebox.setter('height'))
        for i in range(10):
            try:
                word=random.choice(word__)
                box__=self.create_content_box(data_[word][random.choice([i for i in data_[word].keys()])])
                home__.append(box__)
                self.homebox.add_widget(box__)
            except: pass

        self.refreshbutton=MDFillRoundFlatButton(text="Làm mới",size_hint=(None, None), pos_hint={"center_x":0.5, "center_y":0.5}, md_bg_color=btn, theme_text_color="Custom", text_color=secondarycolor)
        self.refreshbutton.bind(on_press=self.refresh)

        self.resultlabel.bind(texture_size=self.resultlabel.setter('text_size'))
        self.resultlabel.bind(texture_size=self.resultlabel.setter('size'))

        self.box = MDBoxLayout(size_hint=(1, None), pos_hint={"center_x":0.5}, height=dp(50))

        self.taskbar=MDCard(md_bg_color=btn, radius=[25, 25, 25, 25], size_hint=(1, None), height=dp(50), pos_hint={"center_x":0.5, "center_y": 0.5})
        self.taskbar.radius=[dp(i) for i in self.taskbar.radius]
        self.button.bind(on_release=self.show_input)
        self.homebutton.bind(on_release=self.home)
        self.menubutton.bind(on_release=self.menu_open)

        self.combine_box.bind(minimum_height=self.combine_box.setter('height'))
        self.combine_box.suggest_box.bind(minimum_height=self.combine_box.suggest_box.setter('height'))
        self.text_input.input.bind(focus=self.hide_input)
        self.text_input.input.bind(text=self.quick_search)

        self.result_template=result_template()
        self.translate_result_template=translate_result_template()

        self.synonyms_box=MDBoxLayout(size_hint_x=None, spacing=dp(20), padding=[dp(10),dp(10),dp(10),dp(10)], pos_hint={'center_y': 0.5})
        self.synonyms=ScrollView(do_scroll_y=False, size_hint=(1,None), height=dp(50))
        self.synonyms_box.bind(minimum_width=self.synonyms_box.setter('width'))

        self.antonyms_box=MDBoxLayout(size_hint_x=None, spacing=dp(20), padding=[dp(10),dp(10),dp(10),dp(10)], pos_hint={'center_y': 0.5})
        self.antonyms=ScrollView(do_scroll_y=False, size_hint=(1,None), height=dp(50))
        self.antonyms_box.bind(minimum_width=self.antonyms_box.setter('width'))

        self.recent = recent(self.create_content_box, self.clear_history, self.noname.radius)
        if len(recent_search)>0:
            for i in recent_search:
                if str(type(recent_search[i]))=="<class 'dict'>":
                    for j in recent_search[i]:
                        self.recent.recent_scrollview_box.add_widget(self.create_content_box(recent_search[i][j]), index=0)
            self.recent.container.add_widget(self.recent.recent_scrollview)
        else:
            self.recent.container.add_widget(self.recent.label)

        self.text_input.add_widget(self.text_input.input)
        self.text_input.add_widget(self.text_input.left_icon)
        self.text_input.add_widget(self.text_input.button)
        self.progress_box.add_widget(self.progress_bar)
        self.add_widget(self.label)
        self.add_widget(self.one_box)
        self.one_box.add_widget(self.noname)
        self.noname.add_widget(self.progress_box)
        self.noname.add_widget(self.scrollview)
        self.scrollview.add_widget(self.homebox)
        self.homebox.add_widget(self.refreshbutton)
        self.add_widget(self.combine_box)
        self.taskbar.add_widget(self.homebutton)
        self.taskbar.add_widget(self.button)
        self.taskbar.add_widget(self.menubutton)
        self.combine_box.add_widget(self.combine_box.suggest_box)
        self.combine_box.add_widget(self.box)
        self.box.add_widget(self.taskbar)
        self.synonyms.add_widget(self.synonyms_box)
        self.antonyms.add_widget(self.antonyms_box)

    def on_folder_len(self, instance, value):
        if value>0:
            instance.result_label.text=f"Có {value} từ vựng"
            try:
                if instance.children[0]!=instance.morebutton:
                    instance.morebutton=MDIconButton(icon="chevron-right", theme_icon_color="Custom", icon_color=primarycolor, pos_hint={"center_x": 0.5, "center_y": 0.5})
                    instance.morebutton.bind(on_press=lambda nah: self.show_fav_folder(nah, instance.result_head_label.text))
                    instance.add_widget(instance.morebutton)
            except:
                instance.morebutton=MDIconButton(icon="chevron-right", theme_icon_color="Custom", icon_color=primarycolor, pos_hint={"center_x": 0.5, "center_y": 0.5})
                instance.morebutton.bind(on_press=lambda nah: self.show_fav_folder(nah, instance.result_head_label.text))
                instance.add_widget(instance.morebutton)
        else:
            instance.result_label.text=f"Không có từ vựng"
            instance.remove_widget(instance.children[0])

    def on_choose_mode(self, instance, value):
        for child in self.favlist.fav_scrollview_box.children:
            if value:
                child.children[-2].icon="check"
                child.children[-2].unbind(on_press=self.renamefav)
                child.children[-2].bind(on_press=self.addfav)
                self.fav_label.text="Chọn danh mục"
                if len(fav_list[child.result_head_label.text])>0: child.remove_widget(child.children[0])
            else:
                child.folder_len+=1
                child.folder_len-=1
                child.children[-2].icon="rename"
                child.children[-2].unbind(on_press=self.addfav)
                child.children[-2].bind(on_press=self.renamefav)
                self.fav_label.text="Yêu thích"

    def copy(self, instance, text=None, copy=None):
        if text:
            synonyms=', '.join(text['synonyms']) if text['synonyms'] else None
            antonyms=', '.join(text['antonyms']) if text['antonyms'] else None
            copy=f"""{text['word'].capitalize()} ({text['type']}):
/{eng_to_ipa.convert(text['word'])}/

{text["definition"][:1].upper()+text["definition"][1:]}
*Từ đồng nghĩa: {f'{synonyms}' if synonyms else 'Không có từ đồng nghĩa'}

*Từ trái nghĩa: {f'{antonyms}' if antonyms else 'Không có từ trái nghĩa'}"""
        elif copy: copy=copy
        pyperclip.copy(copy)

        MDSnackbar(MDLabel(text="Đã sao chép nội dung", theme_text_color="Custom", text_color=primarycolor), md_bg_color=menubg, y=dp(10),  size_hint_x=.85, pos_hint={"center_x": 0.5}, radius=[dp(25), dp(25), dp(25), dp(25)]).open()

    def remove_nav_bar(self):
        self.progress_box.height=dp(5)
        self.progress_box.remove_widget(self.nav_bar)
        self.progress_box.remove_widget(self.fav_nav_bar)

    def refresh_nav_bar(self):
        self.progress_box.height=dp(60)
        self.progress_box.add_widget(self.progress_bar)

    def show_recent(self, *args):
        global current_page
        current_page="recent"
        self.menu.dismiss()
        self.progress_bar.back_color=bg
        self.progress_bar.color=self.progress_bar.back_color
        self.noname.md_bg_color=bg
        self.remove_nav_bar()
        self.scrollview.clear_widgets()
        self.scrollview.add_widget(self.recent)
        fade_in_vertical(self.recent.container)

    def show_fav_folder(self, instance, folder):
        self.fav_label.text=folder
        self.fav_nav_bar.clear_widgets()
        self.fav_nav_bar.add_widget(self.fav_label)
        _content_=content()
        for i in fav_list[folder]:
            _content_.add_widget(self.create_chips(i))
        self.scrollview.clear_widgets()
        self.scrollview.add_widget(_content_)
        fade_in_vertical(_content_)

    def _show_fav_(self, *args):
        self.favlist.choose_mode=False
        self.show_fav()

    def show_fav(self, *args):
        global current_page
        current_page="favorite word list"
        self.menu.dismiss()
        self.progress_box.clear_widgets()
        self.refresh_nav_bar()
        self.progress_box.add_widget(self.fav_nav_bar)
        self.fav_nav_bar.clear_widgets()
        self.fav_nav_bar.add_widget(self.fav_back_button)
        self.fav_nav_bar.add_widget(self.fav_label)
        self.fav_nav_bar.add_widget(self.add_button)
        self.fav_label.text="Yêu thích"
        self.scrollview.scroll_y=1
        self.progress_bar.back_color=(boxbg)
        self.noname.md_bg_color=boxbg
        self.scrollview.do_scroll_x, self.scrollview.do_scroll_y=False, True
        self.scrollview.clear_widgets()
        self.scrollview.add_widget(self.favlist)
        fade_in_vertical(self.favlist)

    def choose_folder(self, instance, word):
        global _key_
        self.favlist.choose_mode=True
        _key_=word
        self.show_fav()

    def addfav(self, instance):
        global _key_
        self.menu.dismiss()
        if _key_ not in fav:
            folder=instance.parent.result_head_label.text
            fav_list[folder].append(_key_)
            fav[_key_]=folder
            self.show_fav()
        else:
            folder=fav[_key_]
            fav_list[folder].remove(_key_)
            del fav[_key_]

        with open(f"func/setting/fav_word_list.txt", "w", encoding="utf-8") as fo:
            fo.write(json.dumps(fav_list, ensure_ascii=False, indent=4))
        folders[folder].folder_len=len(fav_list[folder])
        self.favlist.choose_mode=False
        _key_=None

    def add_fav(self, *args):
        self.fav_dialog.dismiss()
        self.fav_container.text=self.fav_container.text.strip()
        if self.fav_container.text not in fav_list and self.fav_container.text!="":
            fav_list[self.fav_container.text]=[]
            folder_name=self.fav_container.text
            _folder_=folder(self.fav_container.text, "Không có từ vựng")
            _folder_.bind(folder_len=self.on_folder_len)
            folders.update([(self.fav_container.text, _folder_)])
            if self.favlist.choose_mode:
                check=MDIconButton(icon="check", theme_icon_color="Custom", icon_color=primarycolor, pos_hint={"center_x": 0.5, "center_y": 0.5})
                check.bind(on_press=self.addfav)
                _folder_.add_widget(check, index=0)
            else:
                rename=MDIconButton(icon="rename", theme_icon_color="Custom", icon_color=primarycolor, pos_hint={"center_x": 0.5, "center_y": 0.5})
                rename.bind(on_press=self.renamefav)
                _folder_.add_widget(rename)
            _folder_.add_widget(MDIconButton(icon="delete", theme_icon_color="Custom", icon_color=primarycolor, pos_hint={"center_x": 0.5, "center_y": 0.5}, on_press=lambda instance: self.remove_fav(instance)))
            self.favlist.fav_scrollview_box.add_widget(_folder_)
            fade_in_vertical(_folder_)
        with open(f"func/setting/fav_word_list.txt", "w", encoding="utf-8") as fo:
            fo.write(json.dumps(fav_list, ensure_ascii=False, indent=4))
        if len(fav_list)>0:
            self.favlist.container.clear_widgets()
            self.favlist.container.add_widget(self.favlist.fav_scrollview)
        self.fav_container.text=""

    def remove_fav(self, instance):
        global fav_list, fav
        fade_out_vertical(instance.parent, on_complete=self._remove_fav_)

    def _remove_fav_(self, instance):
        global fav_list, fav
        del fav_list[instance.result_head_label.text]
        self.favlist.fav_scrollview_box.remove_widget(instance)
        with open(f"func/setting/fav_word_list.txt", "w", encoding="utf-8") as fo:
            fo.write(json.dumps(fav_list, ensure_ascii=False, indent=4))
        if len(fav_list)==0:
            self.favlist.container.clear_widgets()
            self.favlist.container.add_widget(self.favlist.label)
            fade_in_vertical(self.favlist.label)
        fav=remove_keys_by_value(fav, instance.result_head_label.text)

    def renamefav(self, instance):
        self.instance=instance.parent.result_head_label
        self.fav_rename_container=MDTextField(hint_text="Tên danh mục mới", line_color_normal=boxbg, line_color_focus=menubg, hint_text_color=[0.75-i for i in primarycolor], hint_text_color_focus=primarycolor, text_color_focus=primarycolor, fill_color_normal=boxbg, mode="round", size_hint=(1, None), pos_hint={'center_x': 0.5}, height=dp(30), multiline=False)
        self.fav_rename_container.bind(on_text_validate=self.rename_fav)

        self.fav_rename_dialog=MDDialog(
            title="Đổi tên danh mục",
            type="custom",
            content_cls=self.fav_rename_container,
            buttons=[
                MDFillRoundFlatButton(
                    text="Xác nhận",
                    md_bg_color=btn,
                    theme_text_color="Custom",
                    text_color=secondarycolor,
                    on_press=self.rename_fav
                ),
                MDFillRoundFlatButton(
                    text="Huỷ",
                    md_bg_color=btn,
                    theme_text_color="Custom",
                    text_color=secondarycolor,
                )],
            md_bg_color=boxbg
        )
        self.fav_rename_dialog.buttons[1].bind(on_press=self.fav_rename_dialog.dismiss)
        self.fav_rename_dialog.open()

    def rename_fav(self, instance):
        new_name = self.fav_rename_container.text.strip()
        if new_name and new_name != self.instance.text and new_name not in fav_list:
            items = list(fav_list.items())
            index = items.index((self.instance.text, fav_list[self.instance.text]))
            fav_list[new_name] = fav_list.pop(self.instance.text)
            updated_items = items[:index] + [(new_name, fav_list[new_name])] + items[index + 1:]
            fav_list.clear()
            fav_list.update(updated_items)
            for word in fav_list[new_name]:
                fav[word] = new_name
            with open(f"func/setting/fav_word_list.txt", "w", encoding="utf-8") as fo:
                fo.write(json.dumps(fav_list, ensure_ascii=False, indent=4))
            self.instance.text=new_name
            fade_in_vertical(self.instance)
        self.fav_rename_dialog.dismiss()

    def clear_history(self, instance):
        global recent_search
        recent_search={}
        self.recent.recent_scrollview_box.clear_widgets()
        self.recent.container.clear_widgets()
        self.recent.container.add_widget(self.recent.label)
        fade_in_vertical(self.recent.container)
        with open(f"func/setting/{settings['uid']}.txt", "w", encoding="utf-8") as fo:
            fo.write("{}")

    def create_chips(self, text):
        return MDFillRoundFlatButton(text=text, theme_icon_color='Custom', md_bg_color=btn, theme_text_color="Custom", text_color=secondarycolor, font_name=f"func/setting/fonts/{settings['fonts']}.ttf", font_size=dp(15), on_press=lambda instance: self.search_button_pressed(instance, [text]))

    def create_content_box(self, text):
        self.content_box=content_box(text)
        self.content_box.morebutton=MDFillRoundFlatButton(text="Xem thêm", pos_hint={"center_x":0.5, "center_y":0.5}, md_bg_color=btn, theme_text_color="Custom", text_color=secondarycolor)
        self.content_box.morebutton.on_press=partial(self.search_button_pressed, instance=None, input_text=text['type'], value=False, temp=text)
        self.content_box.add_widget(self.content_box.morebutton)
        return self.content_box

    def _create_content_box_(self, text):
        self.content_box=content_box_(text)
        if text["definition"]!="Không có kết quả":
            self.content_box.morebutton=MDFillRoundFlatButton(text="Xem thêm", pos_hint={"center_y":0.5}, md_bg_color=btn, theme_text_color="Custom", text_color=secondarycolor)
            self.content_box.add_widget(self.content_box.morebutton)
            self.content_box.morebutton.bind(on_press=lambda instance: self.search_button_pressed(instance, [text['word']]))
        return self.content_box

    def add_data(self):
        global current_page
        current_page="add_data"
        self.remove_nav_bar()
        self.menu.dismiss()
        self.progress_bar.back_color=bg
        self.progress_bar.color=self.progress_bar.back_color
        self.noname.md_bg_color=bg
        self.scrollview.clear_widgets()
        self.scrollview.add_widget(self.add_data_)
        fade_in_vertical(self.add_data_)

    def infinite_homepage(self, instance, unknown):
        global generated
        if current_page=="home":
            global _temp_
            if self.scrollview.scroll_y<-0.1:
                self.homebox.remove_widget(self.refreshbutton)
                if len(generated)<5:
                    for i in range(30):
                        try:
                            word=random.choice(word__)
                            generated.append(self.create_content_box(data_[word][random.choice([i for i in data_[word].keys()])]))
                        except: pass
                for i in range(random.randint(1, 10)):
                    try:
                        home__.append(generated[0])
                        self.homebox.add_widget(generated[0])
                        generated=generated[1:]
                    except: pass
                self.homebox.add_widget(self.refreshbutton)

            elif self.scrollview.scroll_y>=1.05:
                self.refresh(None)

    def refresh(self, instance):
        global home__, generated
        word=random.choice(word__)
        generated.append(self.create_content_box(data_[word][random.choice([i for i in data_[word].keys()])]))
        if home__: self.scrollview.scroll_to(home__[0])
        for i in range(len(home__)):
            if not home__[i]._state_: home__[i].viewstate()
            try:
                word=random.choice(word__)
                text=data_[word][random.choice([i for i in data_[word].keys()])]
                home__[i]._text_=text["definition"]
                home__[i].expand_result_head_label.text=text["word"]+" ("+text["type"].lower()+")"+f'\n/{eng_to_ipa.convert(text["word"])}/'
                pos=text["definition"].strip().find('\n')
                if pos!=-1 and pos<=50:
                    home__[i].shrink_result_label.text=text["definition"][:text["definition"].find('\n')]+"..."
                else:
                    home__[i].shrink_result_label.text=text["definition"][:50]
                    if len(text["definition"])>50:
                        home__[i].shrink_result_label.text+="..."
                home__[i].expand_result_label.text=text["definition"]
                home__[i].morebutton.on_press=partial(self.search_button_pressed, instance=None, input_text=text['type'], value=False, temp=text)
            except Exception as e: print(e)
        set_opacity_recursive(self.homebox)
        Animation(opacity=1, duration=0.5).start(self.homebox)

    def menu_open(self, instance):
        menu_items = [
            {
                "text": "Cài đặt",
                "text_color": primarycolor,
                "trailing_icon": "cog",
                "theme_trailing_icon_color": "Custom",
                "trailing_icon_color": primarycolor,
                "on_release": lambda x="Setting": self.go_to_page_2(x)
            },
            {
                "text": "Whoop AI",
                "text_color": primarycolor,
                "trailing_icon": "creation",
                "theme_trailing_icon_color": "Custom",
                "trailing_icon_color": primarycolor,
                "on_release": lambda x="Setting": self.go_to_page_3(x)
            },
            {
                "text": "Dịch thuật",
                "text_color": primarycolor,
                "trailing_icon": "translate",
                "theme_trailing_icon_color": "Custom",
                "trailing_icon_color": primarycolor,
                "on_release": lambda x=None: self.translate(x)
            },
            {
                "text": "Thêm từ vựng",
                "text_color": primarycolor,
                "trailing_icon": "plus-circle",
                "theme_trailing_icon_color": "Custom",
                "trailing_icon_color": primarycolor,
                "on_release": self.add_data
            },
            {
                "text": "Yêu thích",
                "text_color": primarycolor,
                "trailing_icon": "heart",
                "theme_trailing_icon_color": "Custom",
                "trailing_icon_color": primarycolor,
                "on_release": self._show_fav_
            },
            {
                "text": "Gần đây",
                "text_color": primarycolor,
                "trailing_icon": "history",
                "theme_trailing_icon_color": "Custom",
                "trailing_icon_color": primarycolor,
                "on_release": self.show_recent
            }
        ]
        self.menu=MDDropdownMenu(
            caller=self.menubutton,
            items=menu_items,               
            ver_growth="up",
            md_bg_color=menubg,
            position="top"
        )
        self.menu.open()

    def word_option(self, instance):
        global _key_
        word=result[list(result.keys())[0]]['word']
        menu_items = [
            {
                "text_color": primarycolor,
                "theme_trailing_icon_color": "Custom",
                "trailing_icon_color": primarycolor,
            },
            {
                "text": "Gửi đến Whoop AI",
                "text_color": primarycolor,
                "trailing_icon": "creation",
                "theme_trailing_icon_color": "Custom",
                "trailing_icon_color": primarycolor,
                "on_release": self.ai_explain
            },
            {
                "text": "Sao chép",
                "text_color": primarycolor,
                "trailing_icon": "content-copy",
                "theme_trailing_icon_color": "Custom",
                "trailing_icon_color": primarycolor,
                "on_release": lambda instance=instance: self.copy(instance, text=result[list(result.keys())[0]])
            }
        ]
        menu_items[0]["trailing_icon"]="heart-outline"  if word not in fav else "heart"
        menu_items[0]["text"]="Yêu thích"  if word not in fav else "Bỏ yêu thích"
        if word not in fav: menu_items[0]["on_release"]=lambda instance=instance: self.choose_folder(instance, word)
        else:
            _key_=word
            menu_items[0]["on_release"]=lambda instance=instance: self.addfav(instance)
        self.menu=MDDropdownMenu(
            caller=self.copy_button,
            items=menu_items,               
            ver_growth="down",
            hor_growth="left",
            md_bg_color=menubg,
            position="bottom"
        )
        self.menu.open()

    def home(self, instance):
        global _back_, current_page
        if current_page!="home":
            self.progress_bar.back_color=bg
            self.noname.md_bg_color=bg
            self.remove_nav_bar()
            self.scrollview.clear_widgets()
            self.scrollview.add_widget(self.homebox)
            set_opacity_recursive(self.homebox)
            Animation(opacity=1, duration=0.5).start(self.homebox)
        current_page="home"

    def show_input(self, instance):
        self.text_input.input.focus=True
        self.hib.disabled=False
        fade_out_vertical(self.taskbar, on_complete=self._show_input_)

    def _show_input_(self, instance):
        global current_page, result
        self.box.clear_widgets()
        if self.possible_word: self.combine_box.suggest_box.add_widget(self.combine_box.suggest_scroll)
        if self.text_input.input.text.split()!=[] and (self.result_box not in self.scrollview.children) and self.result_box.children: 
            current_page="search"
            self.progress_box.clear_widgets()
            self.refresh_nav_bar()
            self.progress_box.add_widget(self.nav_bar)
            self.scrollview.scroll_y=1
            self.progress_bar.back_color=(boxbg)
            self.noname.md_bg_color=boxbg
            self.scrollview.do_scroll_x, self.scrollview.do_scroll_y=False, True
            self.scrollview.clear_widgets()
            self.scrollview.add_widget(self.result_box)
            fade_in_vertical(self.result_box)
        self.box.add_widget(self.text_input)
        self.box.add_widget(self.hib)
        fade_in_vertical(self.box)

    def hide_input(self, instance, value):
        if (((len(self.text_input.input.text)==0) and (not value)) or self.signal) and self.text_input in self.box.children:
            self.hib.disabled=True
            fade_out_vertical(self.text_input, on_complete=lambda instance: self._hide_input_(instance, value))
        self.signal=False

    def _hide_input_(self, instance, value):
        self.combine_box.suggest_box.clear_widgets()
        self.box.clear_widgets()
        self.box.add_widget(self.taskbar)
        fade_in_vertical(self.box)

    def quick_search(self, instance, value):
        if self.search_thread:
            self.search_event.set()
            self.search_thread.join()
        if self.text_input.input.text!="":
            self.search_event.clear() 
            self.search_thread = threading.Thread(target=self.delay)
            self.search_thread.start()
        else:
            self.progress_bar.color=self.progress_bar.back_color
            self.progress_bar.stop()
            self.home(instance)
        self.text=self.text_input.input.text
        
    def ai_explain(self):
        self.menu.dismiss()
        sm.current = 'third'
        _=sm.get_screen('third')
        text=result[list(result.keys())[0]]
        synonyms=', '.join(text['synonyms']) if text['synonyms'] else None
        antonyms=', '.join(text['antonyms']) if text['antonyms'] else None
        _.layout.text_input.input.multiline=True
        _.layout.text_input.input.text=f"""Explain this:\n
{text['word'].capitalize()} ({text['type']}):

{text["definition"][:1].upper()+text["definition"][1:]}
[*]Synonyms: {f'{synonyms}' if synonyms else 'No synonyms'}

[*]Antonyms: {f'{antonyms}' if antonyms else 'No antonyms'}"""
        _.layout.send_message(None)
        _.layout.text_input.input.multiline=False
        pass
        
    def delay(self):
        if not self.search_event.wait(1): # Wait for 1 second or until the event is set
            if settings["input feature"]=="suggest":
                Clock.schedule_once(self.suggest)
            elif settings["input feature"]=="search":
                self.search_button_pressed(None, word_detector(spelling_checker_for_SOD(" ".join(self.text_input.input.text.lower().split()))))

    def suggest(self, instance):
        self.possible_word=possible(self.text_input.input.text.lower().split()[-1])
        self.combine_box.suggest_box.clear_widgets()
        self.combine_box.suggest_scroll=suggest(self.possible_word)
        if self.possible_word:
            self.combine_box.suggest_box.add_widget(self.combine_box.suggest_scroll)
        
    def translate(self, instance):
        global current_page
        current_page="translate"
        self.progress_bar.back_color=bg
        self.scrollview.clear_widgets()
        self.scrollview.add_widget(self.translate_result_template)
        self.noname.md_bg_color=bg
        self.remove_nav_bar()
        if self.text_input.input.text!="":
            self.signal=True
            self.hide_input(None, None)
        if instance!=None:
            if check_connection():
                try:
                    self.translate_result_template.src_text.text=self.text_input.input.text
                except:
                    self.alert.open()
            else:
                self.no_internet_alert.open()
        else: self.menu.dismiss()
                

    def back(self, instance):
        global _back_
        if len(_back_)>=2:
            if str(type(_back_[-2]))!="<class 'dict'>": self.search_button_pressed(None, _back_[-2], value=False, callback=True)
            else:
                if 'type' in list(_back_[-2].keys()): self.search_button_pressed(None, _back_[-2]["type"], value=False, callback=True, temp=_back_[-2])
                else: self.search_button_pressed(None, None, value=False, callback=True, temp=_back_[-2])
        _back_=_back_[::-1][1:][::-1]
        if len(_back_)<2: 
            self.back_button.disabled=True

    def search_button_pressed(self, instance, input_text, value=True, callback=False, temp=False):
        global _value_, _callback_
        if not value: _value_=value
        if callback: _callback_=callback
        try: self.recent.dismiss()
        except: pass
        threading.Thread(target=self.search, args=(instance, input_text, temp)).start()
        self.progress_bar.color=btn
        self.progress_bar.start()

    def search(self, instance, input_text, temp):
        global result
        self.scrollview.do_scroll_x, self.scrollview.do_scroll_y=False, True
        if not temp:
            self.input_text=input_text
            result=SOD(self.input_text, database=data_, database_path=f"func/data/tu_dien_nguon.txt", get_database_from_path=False, internet=check_connection())
            if len(result)==1:
                result=result[input_text[0]]
                Clock.schedule_once(self.update_UI)
            else:
                Clock.schedule_once(self._update_UI_)
        else:
            if input_text!=None:
                self.input_text=[temp["word"]]
                result={input_text: temp}
            else:
                self.input_text=[temp[list(temp.keys())[0]]['word']]
                result=temp
            Clock.schedule_once(self.update_UI)

    def _update_UI_(self, instance):
        global result, recent_search, _value_, _callback_, current_page
        current_page="search"
        self.progress_box.clear_widgets()
        self.refresh_nav_bar()
        self.progress_box.add_widget(self.nav_bar)
        self.nav_bar.clear_widgets()
        self.nav_bar.add_widget(self.back_button)
        self.scrollview.scroll_y=1
        self.progress_bar.back_color=(boxbg)
        self.noname.md_bg_color=boxbg
        self.scrollview.do_scroll_x, self.scrollview.do_scroll_y=False, True
        self.scrollview.clear_widgets()
        self.result_box.clear_widgets()
        if str(type(result))=="<class 'dict'>":
            for rlt in result:
                temp_value={"word": rlt, "type": "", "definition": "", "synonyms": [], "antonyms": []}
                if result[rlt]=="Không có kết nối mạng và không có sẵn trong bộ dữ liệu ofline" or result[rlt]=="Không tìm thấy từ": temp_value["definition"]="Không có kết quả"
                else: temp_value["definition"]=f"Có {len(result[rlt])} kết quả"
                self.result_box.add_widget(self._create_content_box_(temp_value))
        if not _callback_:
            try:
                if self.input_text!=_back_[-1]: _back_.append(self.input_text)
            except:
                _back_.append(self.input_text)
        else: _callback_=not _callback_
        try:
            if len(_back_)>1:
                self.back_button.disabled=False
        except: pass
        self.scrollview.add_widget(self.result_box)
        fade_in_vertical(self.result_box)
        self.progress_bar.color=self.progress_bar.back_color
        self.progress_bar.stop()

    def update_UI(self, instance):
        global result, recent_search, _value_, _callback_, current_page
        current_page="search"
        self.scrollview.scroll_y=1
        self.progress_bar.back_color=(boxbg)
        self.noname.md_bg_color=boxbg
        self.scrollview.do_scroll_x, self.scrollview.do_scroll_y=False, True
        self.scrollview.clear_widgets()
        self.result_box.clear_widgets()
        if str(type(result))=="<class 'dict'>":
            if len(result)==1:
                for i in result:
                    if len(result)==1:
                        self.progress_box.clear_widgets()
                        self.refresh_nav_bar()
                        self.progress_box.add_widget(self.nav_bar)
                        self.result_template.word.text=self.input_text[0].capitalize()+f' ({i.lower()})'
                        self.nav_bar.clear_widgets()
                        self.copy_button=MDIconButton(icon="dots-vertical", theme_icon_color="Custom", icon_color=primarycolor, pos_hint={"x": 1, "center_y": 0.5}, on_press=self.word_option)
                        self.nav_bar.add_widget(self.back_button)
                        self.nav_bar.add_widget(self.result_template.word)
                        self.nav_bar.add_widget(self.copy_button)
                        self.result_template.pronunciation_button.on_release=partial(self.pronounce, instance, self.input_text[0])
                        self.result_template.pronunciation.text=f'/{eng_to_ipa.convert(self.input_text[0])}/'
                        self.result_template.definition.text=result[i]["definition"][:1].upper()+result[i]["definition"][1:]
                        self.result_box.add_widget(self.result_template)
                        self.synonyms_box.clear_widgets()
                        self.synonyms.scroll_x=0
                        head=MDFillRoundFlatButton(text="Từ đồng nghĩa", font_name=f"func/setting/fonts/{settings['fonts']}.ttf", font_size=dp(15), size_hint=(None,None),  pos_hint={"center_x":0.5}, theme_text_color="Custom", text_color=primarycolor, md_bg_color=boxbg, on_press=lambda instance: self.copy(instance, copy=", ".join(result[i]["synonyms"])))
                        if result[i]["synonyms"]!=[]:
                            self.result_box.add_widget(head)
                            self.result_box.add_widget(self.synonyms)
                            for j in result[i]["synonyms"]:
                                self.synonyms_box.add_widget(self.create_chips(j))

                        self.antonyms_box.clear_widgets()
                        self.antonyms.scroll_x=0
                        head=MDFillRoundFlatButton(text="Từ trái nghĩa", font_name=f"func/setting/fonts/{settings['fonts']}.ttf", font_size=dp(15), size_hint=(None,None),  pos_hint={"center_x":0.5}, theme_text_color="Custom", text_color=primarycolor, md_bg_color=boxbg, on_press=lambda instance: self.copy(instance, copy=", ".join(result[i]["antonyms"])))
                        if result[i]["antonyms"]!=[]:
                            self.result_box.add_widget(head)
                            self.result_box.add_widget(self.antonyms)
                            for j in result[i]["antonyms"]:
                                self.antonyms_box.add_widget(self.create_chips(j))
                        if not _callback_:
                            try:
                                if result[i]!=_back_[-1]: _back_.append(result[i])
                            except:
                                _back_.append(result[i])
                        else: _callback_=not _callback_
                        try:
                            if len(_back_)>1:
                                self.back_button.disabled=False
                        except: pass
            else:
                self.progress_box.clear_widgets()
                self.refresh_nav_bar()
                self.progress_box.add_widget(self.nav_bar)
                self.nav_bar.clear_widgets()
                self.nav_bar.add_widget(self.back_button)
                for i in result:
                    self.result_box.add_widget(self.create_content_box(result[i]))
                if not _callback_:
                    try:
                        if result!=_back_[-1]: _back_.append(result)
                    except:
                        _back_.append(result)
                else: _callback_=not _callback_
                try:
                    if len(_back_)>1:
                        self.back_button.disabled=False
                except: pass
            if self.input_text[0] not in recent_search:
                if len(recent_search)==0:
                    self.recent.container.clear_widgets()
                    self.recent.container.add_widget(self.recent.recent_scrollview)
                for i in result:
                    self.recent.recent_scrollview_box.add_widget(self.create_content_box(result[i]), index=0)
                recent_search[self.input_text[0]]=result
        else:
            self.nav_bar.clear_widgets()
            self.nav_bar.add_widget(self.back_button)
            self.resultlabel.text = "".join(result)
            self.result_box.add_widget(self.resultlabel)
            if not _callback_:
                try:
                    if result!=_back_[-1]: _back_.append(result)
                except:
                    _back_.append(result)
            else: _callback_=not _callback_
            try:
                if len(_back_)>1:
                    self.back_button.disabled=False
            except: pass

        with open(f"func/setting/{settings['uid']}.txt", "w", encoding="utf-8") as fo:
            fo.write(json.dumps(recent_search, ensure_ascii=False, indent=4))
        if _value_ and check_connection(): threading.Thread(target=track_user_queries, args=({self.input_text[0]: result},)).start()
        else: _value_=not _value_
        self.scrollview.add_widget(self.result_box)
        set_opacity_recursive(self.result_template.word)
        Animation(opacity=1, duration=0.5).start(self.result_template.word)
        fade_in_vertical(self.result_box)
        self.progress_bar.color=self.progress_bar.back_color
        self.progress_bar.stop()

    def pronounce(self, instance, text):
        self.result_template.pronunciation_button.disabled=True
        threading.Thread(target=self.run, args=[text, ]).start()

    def run(self, text):
        if engine:
            engine.say(text)
            engine.runAndWait()
            engine.stop()
        else:
            try: tts = gTTS(text)
            except:Clock.schedule_once(self.no_internet_alert.open)
            else:
                file_name="temp.wav"
                tts.save(file_name)
                sound = SoundLoader.load(file_name)
                if sound:
                    sound.play()
                    if os.path.exists(file_name):
                        os.remove(file_name)

        Clock.schedule_once(self.eb)

    def eb(self, instance):
        self.result_template.pronunciation_button.disabled=False

    def go_to_page_2(self, instance):
        self.menu.dismiss()
        sm.current = 'second'
        
    def go_to_page_3(self, instance):
        self.menu.dismiss()
        sm.current = 'third'

    def on_double_tap(self, instance, *args):
        if self.text_input.input.text.strip()!="":
            if self.text_input in self.box.children:    
                self.text=self.text_input.input.text
                self.signal=True
                self.hide_input(instance, False)
            else:
                self.show_input(instance)
