from ui import *

class update_dialog(MDBottomSheet):
    def __init__(self, **kwargs):
        super(update_dialog, self).__init__(**kwargs)
        self.padding=[dp(20), dp(20), dp(20), dp(20)]
        self.radius=[dp(25), dp(25), dp(25), dp(25)]
        self.bg_color=bg
        self.size_hint=(None, None)
        self.height=dp(180)
        self.width=dp(400)
        self.pos_hint={"center_x": 0.5}
        self.container=MDBoxLayout(spacing=dp(20), pos_hint={"center_x": 0.5})
        self.official=MDCard(orientation="vertical", padding=[dp(10), dp(10), dp(10), dp(10)] , radius=[dp(25), dp(25), dp(25), dp(25)], md_bg_color=boxbg, size_hint=(0.5, 1), pos_hint={"top": 1}, ripple_behavior=True)
        self.official.add_widget(MDIcon(icon="web", pos_hint={"center_x": 0.5, "y": 1}))
        self.official.add_widget(MDLabel(text=f"[b]Chính thức[/b]", pos_hint={"center_x": 0.5}, halign="center", valign="top", size_hint=(1, None), height=dp(30), markup=True))
        self.official.add_widget(MDLabel(text=f"[size={int(dp(12))}]Truy cập vào phiên bản dữ liệu ngoại tuyến chính thức[/size]", pos_hint={"center_x": 0.5}, halign="center", valign="top", size_hint=(1, 1), markup=True))
        self.early_access=MDCard(orientation="vertical", padding=[dp(10), dp(10), dp(10), dp(10)] , radius=[dp(25), dp(25), dp(25), dp(25)], md_bg_color=boxbg, size_hint=(0.5, 1), pos_hint={"top": 1}, ripple_behavior=True)
        self.early_access.add_widget(MDIcon(icon="clock-fast", pos_hint={"center_x": 0.5, "y": 1}))
        self.early_access.add_widget(MDLabel(text=f"[b]Truy cập sớm[/b]", pos_hint={"center_x": 0.5}, halign="center", valign="top", size_hint=(1, None), height=dp(30), markup=True))
        self.early_access.add_widget(MDLabel(text=f"[size={int(dp(12))}]Truy cập sớm vào phiên bản dữ liệu ngoại tuyến mới nhất, tuy nhiên tốc độ cập nhật chậm hơn[/size]", pos_hint={"center_x": 0.5}, halign="center", valign="top", size_hint=(1, 1), markup=True))
        self.container.add_widget(self.official)
        self.container.add_widget(self.early_access)
        self.add_widget(self.container)
