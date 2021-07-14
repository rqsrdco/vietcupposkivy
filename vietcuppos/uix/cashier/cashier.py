from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.properties import ObjectProperty, StringProperty
from kivy.metrics import dp
from kivy.utils import get_color_from_hex as C

from kivymd.uix.list import OneLineListItem
from kivymd.theming import ThemableBehavior
from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.snackbar import Snackbar

from vietcuppos.uix.mdicons import PreviousMDIcons
from vietcuppos.uix.billitem import BillItem


class BillsMenuHeader(MDBoxLayout):
    pass


class CashierLeftScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        print("---|CashierScreenManager| --- |__init__|---")
        self.transition = NoTransition()

        self.add_widget(PreviousMDIcons())


class CashierWindow(ThemableBehavior, MDScreen):
    left_cashier_scrn_mgr = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("---|CashierWindow| --- |__init__|---")

        self.name = 'cashier'
        self.left_cashier_scrn_mgr = CashierLeftScreenManager()
        self.ids.left_navigation_contents.add_widget(
            self.left_cashier_scrn_mgr)

        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"Bills {i}",
                "height": dp(52),
                "on_release": lambda x=f"Bills {i}": self.menu_callback(x), } for i in range(5)
        ]

        self.menu = MDDropdownMenu(
            background_color=("#382B2A0f"),
            header_cls=BillsMenuHeader(),
            position="bottom",
            items=menu_items,
            width_mult=4,
        )

    def remove_item(self, instance):
        self.ids.md_list.remove_widget(instance)

    def open_menu(self, button):
        self.menu.caller = button
        self.menu.open()

    def menu_callback(self, text_item):
        self.menu.dismiss()
        Snackbar(text=text_item).open()

    def on_pre_enter(self, *args):
        print("---|CashierWindow| --- |on_pre_enter|---")
        self.ids.list_coffee.clear_widgets()
        for x in range(50):
            self.ids.list_coffee.add_widget(
                OneLineListItem(
                    text=f"Coffee {x}",
                )
            )
        return super().on_enter(*args)

    def on_enter(self):
        print("---|CashierWindow| --- |on_enter|---")
        for i in range(20):
            self.ids.md_list.add_widget(
                BillItem(
                    title=f"One-line item {i}",
                    count=i,
                    price=str(i * 23000)
                )
            )

    def change_left_scrn(self, screen):
        if self.left_cashier_scrn_mgr.has_screen(screen):
            self.left_cashier_scrn_mgr.current = screen
        else:
            pass
