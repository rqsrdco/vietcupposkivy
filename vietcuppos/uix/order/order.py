from kivymd.uix.screen import MDScreen


class OrderScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.name = "orderscreen"
