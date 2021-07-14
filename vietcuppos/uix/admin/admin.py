from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.theming import ThemableBehavior


class ItemBackdropBackLayer(ThemableBehavior, BoxLayout):
    icon = StringProperty("android")
    text = StringProperty()
    selected_item = BooleanProperty(False)

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            for item in self.parent.children:
                if item.selected_item:
                    item.selected_item = False
            self.selected_item = True
        return super().on_touch_down(touch)


class AdminWindow(ThemableBehavior, MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("---|AdminWindow| --- |__init__|---")

        self.name = 'admin'

    def on_pre_enter(self, *args):
        print("---|AdminWindow| --- |on_pre_enter|---")

    def on_enter(self):
        print("---|AdminWindow| --- |on_enter|---")
        #app = MDApp.get_running_app()
        # print(app.root.screens)


class AdminApp(MDApp):
    def build(self):
        self.title = ""
        return AdminWindow()

    def show_signout_dialog(self):
        pass


if __name__ == '__main__':
    AdminApp().run()
