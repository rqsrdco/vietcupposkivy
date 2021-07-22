from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.utils import get_color_from_hex as ColorHex

import os


from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFlatButton

from vietcuppos.app import POSApp
from vietcuppos.uix.sweetalert import SweetAlert

from vietcuppos.uix.auth import LoginScreen
from vietcuppos.uix.admin import AdminWindow
from vietcuppos.uix.cashier import CashierWindow

from vietcuppos.uix.mdicons import PreviousMDIcons


class MainApp(POSApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.title = "VietCup Coffee POS"
        self.icon = "vietcuppos/images/logo.png"

        self.use_kivymd = True

        self.theme_manager.bg_color = ColorHex(
            "#382B2A")  # (0.8, 0.8, 0.85)
        self.theme_manager.light_color = ColorHex(
            "#E3BFA3")  # (0.9, 0.9, 0.95, 1)
        self.theme_manager.dark_color = ColorHex(
            "#2B2A29")  # (0.6, 0.6, 0.65, 1)
        self.theme_manager.text_color = ColorHex(
            "#F1E9C6")  # (0.5, 0.2, 0.9, 1)
        self.theme_manager.primary_color = ColorHex("#E6C67C")

        self.app_scrn_mgr.add_widget(LoginScreen())
        self.app_scrn_mgr.add_widget(CashierWindow())
        self.app_scrn_mgr.add_widget(AdminWindow())
        self.app_scrn_mgr.add_widget(PreviousMDIcons())
        Window.clearcolor = ColorHex("#382B2A00")
        return self.app_scrn_mgr

    def on_start(self):
        self.root.current = 'auth'

    def show_alert(self):
        self.alert = SweetAlert()
        self.alert.fire(
            buttons=[
                MDFlatButton(
                    text='OK',
                    font_size=16,
                    on_release=self.sign_out,
                )
            ],
            type="question",
            footer="Are you want to signout ?"
        )

    def sign_out(self, *args):
        self.root.current = 'auth'

    def show_theme_picker(self):
        '''Display a dialog window to change app's color and theme.'''
        self.theme_dialog.open()


if __name__ == "__main__":
    MainApp().run()
