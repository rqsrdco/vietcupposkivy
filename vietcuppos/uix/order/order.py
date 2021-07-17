from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.screen import MDScreen
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.list import OneLineListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.toast import toast
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFlatButton, MDIconButton
from kivymd.uix.card import MDCard

from kivy.properties import ObjectProperty, ListProperty, StringProperty, NumericProperty, DictProperty
from kivy.utils import get_color_from_hex as ColorHex
from kivy.utils import get_color_from_hex as C
from kivy.uix.modalview import ModalView
from kivy.uix.label import Label
from kivy.factory import Factory
from kivy.clock import Clock
from kivy.metrics import dp

import time
from functools import partial

from vietcuppos.uix.components import ItemBill, ItemMenu


class OrderScreen(MDScreen):

    recent_bill = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.name = "orderscreen"

    def on_enter(self, *args):
        self.get_menu_coffee()
        self.get_menu_drink()
        self.get_menu_foods()

        Clock.schedule_interval(self.update_clock, 1)

    def on_leave(self, *args):
        self.ids.boarding.reset()
        Clock.unschedule(self.update_clock)

    def update_clock(self, *args):
        self.ids.time_stamp.text = time.strftime("%c")

    def remove_item_bill(self, item):
        self.recent_bill.remove_widget(item)

    def clear_bills(self):
        self.recent_bill.clear_widgets()

    def get_menu_coffee(self):
        from kivymd.app import MDApp
        dbsql = MDApp.get_running_app().local_sqlite
        menu_data = dbsql.extractAllData('Menus', order_by='name')
        self.ids.coffee_selectionlist.clear_widgets()
        for coffee in menu_data:
            self.ids.coffee_selectionlist.add_widget(
                ItemMenu(
                    first_label="%s" % coffee[2],
                    second_label="%d" % (coffee[3] * 12345.67),
                    source="vietcuppos/images/logo.png",
                )
            )

    def get_menu_drink(self):
        self.ids.drink_selectionlist.clear_widgets()
        for x in range(20):
            self.ids.drink_selectionlist.add_widget(
                ItemMenu(
                    first_label="Drinking %d" % x,
                    second_label="%d" % (x * 12345.67),
                    source="vietcuppos/images/logo.png",
                )
            )

    def get_menu_foods(self):
        self.ids.foods_selectionlist.clear_widgets()
        for x in range(39):
            self.ids.foods_selectionlist.add_widget(
                ItemMenu(
                    first_label="Foods %d" % x,
                    second_label="%d" % (x * 12345.67),
                    source="vietcuppos/images/logo.png",
                )
            )

    def clear_callback(self, *args):
        coffee = self.ids.coffee_selectionlist.get_selection()
        drink = self.ids.drink_selectionlist.get_selection()
        foods = self.ids.foods_selectionlist.get_selection()
        if not bool(coffee) is not True:
            self.ids.coffee_selectionlist.clear_selection()
        if not bool(drink) is not True:
            self.ids.drink_selectionlist.clear_selection()
        if not bool(foods) is not True:
            self.ids.foods_selectionlist.clear_selection()
        #toast("clear_callback : %s %s %s" % (coffee, drink, foods))

    def select_all_callback(self):
        # thieu check current slide
        self.ids.coffee_selectionlist.select_all()
        self.ids.drink_selectionlist.select_all()
        self.ids.foods_selectionlist.select_all()
        toast("select_all_callback")

    def ok_callback(self):
        # Add Items to Order Bill
        coffee = self.ids.coffee_selectionlist.get_selection()
        drink = self.ids.drink_selectionlist.get_selection()
        foods = self.ids.foods_selectionlist.get_selection()

        # coffee
        if not bool(coffee) is not True:
            for key, value in coffee.items():
                self.ids.recent_bill.add_widget(
                    ItemBill(
                        item_name=key,
                        item_amount=1,
                        item_price=float(value),
                        on_delete=self.remove_item_bill()
                    )
                )
        # drink
        if not bool(drink) is not True:
            for key, value in drink.items():
                self.ids.recent_bill.add_widget(
                    ItemBill(
                        item_name=key,
                        item_amount=1,
                        item_price=float(value),
                        on_delete=self.remove_item_bill()
                    )
                )
        # foods
        if not bool(foods) is not True:
            for key, value in foods.items():
                self.ids.recent_bill.add_widget(
                    ItemBill(
                        item_name=key,
                        item_amount=1,
                        item_price=float(value),
                        on_delete=self.remove_item_bill()
                    )
                )
