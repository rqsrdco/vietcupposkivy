from kivymd.toast import toast
from kivymd.uix.screen import MDScreen


class Intros(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.name = "intros"

    def finish_callback(self):
        #toast("Finish callback")
        self.parent.current = 'orderscreen'
