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
from kivy.event import EventDispatcher
from vietcuppos.uix.components import ItemBill, ItemMenu, ListItemMenu
from kivymd.app import MDApp


class OrderItem(ItemMenu):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_press=self._curr_choosen)

    def _curr_choosen(self, event):
        self.parent._curr_order_to_pay = self.first_label
        self._selection_anim()


class ListOrderMenu(ListItemMenu, EventDispatcher):
    _curr_order_to_pay = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type("on_order_pressed_toPay")

    def on__curr_order_to_pay(self, obj, value):
        self.clear_icon_check()
        self.dispatch("on_order_pressed_toPay")

    def clear_icon_check(self):
        if not self.children:
            return
        for child in self.children:
            if child.first_label != self._curr_order_to_pay or child.first_label is not self._curr_order_to_pay:
                child._deselection_anim()
            else:
                child._selection_anim()

    def on_order_pressed_toPay(self, *args):
        pass


class OrderScreen(MDScreen):

    bill_fnc = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.name = "orderscreen"

    def on_enter(self, *args):
        self.get_menu_coffee()
        self.get_menu_drink()
        self.get_menu_foods()
        self.get_orders_not_pay()

    def on_leave(self, *args):
        self.ids.menu_op.reset()

    def get_menu_coffee(self):
        dbsql = MDApp.get_running_app().local_sqlite
        menu_data = dbsql.extractAllData('Menus', order_by='name')
        self.ids.coffee_selectionlist.clear_widgets()
        for coffee in menu_data:
            self.ids.coffee_selectionlist.add_widget(
                ItemMenu(
                    first_label="%s" % coffee[2],
                    second_label="%d" % (coffee[3] * 12345.67),
                    source="vietcuppos/images/coffee.png",
                )
            )

    def get_menu_drink(self):
        self.ids.drink_selectionlist.clear_widgets()
        for x in range(20):
            self.ids.drink_selectionlist.add_widget(
                ItemMenu(
                    first_label="Drinking %d" % x,
                    second_label="%d" % (x * 12345.67),
                    source="vietcuppos/images/drink.png",
                )
            )

    def get_menu_foods(self):
        self.ids.foods_selectionlist.clear_widgets()
        for x in range(39):
            self.ids.foods_selectionlist.add_widget(
                ItemMenu(
                    first_label="Foods %d" % x,
                    second_label="%d" % (x * 12345.67),
                    source="vietcuppos/images/food.png",
                )
            )

    def clear_callback(self, *args):
        self.ids.coffee_selectionlist.clear_selection()
        self.ids.drink_selectionlist.clear_selection()
        self.ids.foods_selectionlist.clear_selection()

    def select_all_callback(self):
        # thieu check current slide
        self.ids.coffee_selectionlist.select_all()
        self.ids.drink_selectionlist.select_all()
        self.ids.foods_selectionlist.select_all()
        toast("select_all_callback")

    def ok_callback(self):
        # Add Items to Order Bill
        # coffee
        coffee = self.ids.coffee_selectionlist.get_selection()
        if len(coffee) >= 1:
            for key, value in coffee.items():
                self.ids.bill_op.add_widget(
                    ItemBill(
                        item_name=key,
                        item_amount=1,
                        item_price=float(value),
                    )
                )
        # drink
        drink = self.ids.drink_selectionlist.get_selection()
        if len(drink) >= 1:
            for key, value in drink.items():
                self.ids.bill_op.add_widget(
                    ItemBill(
                        item_name=key,
                        item_amount=1,
                        item_price=float(value),
                    )
                )
        # foods
        foods = self.ids.foods_selectionlist.get_selection()
        if len(foods) >= 1:
            for key, value in foods.items():
                self.ids.bill_op.add_widget(
                    ItemBill(
                        item_name=key,
                        item_amount=1,
                        item_price=float(value),
                    )
                )

    def qrcode_callback(self, *args):
        toast("qrcode")

    def print_bill_callback(self, *args):
        toast("print")

    def paying_callback(self, *args):
        toast("pay")

    def signal_saved_curr_order(self):
        self.get_orders_not_pay()

    def list_to_dict(self, input_list):
        output_dict = {}
        code = input_list[0][1]
        output_dict["%s" % code] = {}
        num = 1
        for row in input_list:
            dic_r = {}
            dic_r["name"] = row[2]
            dic_r["count"] = row[3]
            dic_r["price"] = row[4]
            if (row[1] == code or row[1] is code):
                output_dict["%s" % code]["%d" % num] = dic_r
                num += 1
            else:
                num = 1
                code = row[1]
                output_dict["%s" % code] = {}
                output_dict["%s" % code]["%d" % num] = dic_r
                num += 1
        return output_dict

    def get_orders_not_pay(self):
        dbsql = MDApp.get_running_app().local_sqlite
        order_wait = dbsql.extractAllData('Orders', order_by='order_code')
        if not order_wait:
            return
        else:
            rslt_dict = self.list_to_dict(order_wait)
            self.ids.order_selectionlist.clear_widgets()
            for key, value in rslt_dict.items():
                _total_price = 0
                for k, v in value.items():
                    _total_price += v["count"] * v["price"]
                self.ids.order_selectionlist.add_widget(
                    OrderItem(
                        first_label="%s" % key,
                        second_label="%d" % _total_price,
                        source="vietcuppos/images/order.png",
                    )
                )

    def show_order_to_pay(self, *args):
        # print(self.ids.order_selectionlist._curr_order_to_pay)
        db = MDApp.get_running_app().local_sqlite
        conn = db.connect_database()
        #_condition = "order_code=%s" % args[0]._curr_order_to_pay
        _order_to_pay = db.search_from_database(
            "Orders", conn, "order_code", args[0]._curr_order_to_pay)
        if len(_order_to_pay) >= 1:
            self.ids.bill_op.clear_current_bill()
            for order in _order_to_pay:
                self.ids.bill_op.add_widget(
                    ItemBill(
                        item_name=order[2],
                        item_amount=order[3],
                        item_price=order[4],
                    )
                )
        else:
            toast("Order Empty !")
