from ui import *

class change_layout(ScrollView):
    def __init__(self, create_layout_preview, **kwargs):
        super(change_layout, self).__init__(**kwargs)
        self.do_scroll_y=False
        self.size_hint=(1, None)
        self.height=125*scale
        self.layout_list=MDBoxLayout(size_hint=(None, 1), pos_hint={"center_x": 0.5}, spacing=20*scale, padding=[10*scale, 10*scale, 10*scale, 10*scale])
        self.layout_list.height=self.layout_list.height*scale
        self.layout_list.bind(minimum_width=self.layout_list.setter('width'))
        self.add_widget(self.layout_list)
        self.layout_list.add_widget(create_layout_preview("box"))
        self.layout_list.add_widget(create_layout_preview("flashcard"))