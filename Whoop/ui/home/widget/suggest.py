from ui import *
import ui

class suggest(ScrollView):
    def __init__(self, suggest_list, **kwargs):
        super(suggest, self).__init__(**kwargs)
        self.do_scroll_y=False
        self.size_hint=(1, None)
        self.height=dp(50)
        self.suggest_list=MDBoxLayout(size_hint=(None, 1), pos_hint={"center_x": 0.5}, spacing=dp(20), padding=[dp(10), dp(10), dp(10), dp(10)])
        self.suggest_list.height=dp(self.suggest_list.height)
        self.suggest_list.bind(minimum_width=self.suggest_list.setter('width'))
        self.add_widget(self.suggest_list)
        for i in suggest_list:
            self.suggest_list.add_widget(self.create_preview(i))

    def create_preview(self, i):
        self.suggest=MDFillRoundFlatButton(text=i, theme_icon_color='Custom', md_bg_color=btn, theme_text_color="Custom", text_color=secondarycolor)
        self.suggest.bind(on_release=lambda instance: self.apply_suggest(instance, i))

        return self.suggest

    def apply_suggest(self, instance, i):
        self.parent.parent.parent.text_input.input.text=" ".join(self.parent.parent.parent.text_input.input.text.split()[:-1]+[i])
        self.parent.parent.parent.text_input.input.focus=True
        self.parent.parent.parent.possible_word=[]