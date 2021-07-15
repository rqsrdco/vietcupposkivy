from kivy.uix.screenmanager import ScreenManager, SwapTransition
from kivy.properties import ObjectProperty
from kivy.metrics import dp
from kivy.utils import get_color_from_hex as C

from kivymd.theming import ThemableBehavior
from kivymd.uix.screen import MDScreen

from vietcuppos.uix.order import OrderScreen
from vietcuppos.uix.intros import Intros


class CashierLeftScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        print("---|CashierScreenManager| --- |__init__|---")
        self.transition = SwapTransition()


class CashierWindow(ThemableBehavior, MDScreen):
    left_cashier_scrn_mgr = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("---|CashierWindow| --- |__init__|---")

        self.name = 'cashier'
        self.left_cashier_scrn_mgr = CashierLeftScreenManager()
        self.left_cashier_scrn_mgr.add_widget(OrderScreen())
        self.left_cashier_scrn_mgr.add_widget(Intros())
        self.ids.left_navigation_contents.add_widget(
            self.left_cashier_scrn_mgr)

    def change_left_scrn(self, screen):
        if self.left_cashier_scrn_mgr.has_screen(screen):
            self.left_cashier_scrn_mgr.current = screen
        else:
            pass
