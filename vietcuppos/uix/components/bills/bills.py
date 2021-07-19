from kivymd.uix.gridlayout import MDGridLayout
from kivymd.theming import ThemableBehavior

from kivy.properties import ObjectProperty, ListProperty, StringProperty, NumericProperty, DictProperty
from kivy.utils import get_color_from_hex as ColorHex
from kivy.event import EventDispatcher
from kivy.clock import Clock
import time
from vietcuppos.uix.components import ItemBill
from kivymd.toast import toast


class BillsOperation(ThemableBehavior, MDGridLayout, EventDispatcher):
    subtotal = NumericProperty(0.0)
    tax = NumericProperty(0.0)
    total = NumericProperty(0.0)

    def __init__(self, **kwargs):
        super(BillsOperation, self).__init__(**kwargs)
        self.register_event_type("on_scan_qrcode")
        self.register_event_type("on_print_bill")
        self.register_event_type("on_paying")
        self.register_event_type("on_save_curr_order")
        Clock.schedule_interval(self.update_clock, 1)

    def update_clock(self, *args):
        self.ids.time_stamp.text = time.strftime("%c")

    def add_widget(self, widget):
        if issubclass(widget.__class__, ItemBill):
            self.ids.list_cur_bill._add_ItemBill(widget)
        else:
            super().add_widget(widget)

    def update_preview(self):
        list_bl = self.ids.list_cur_bill.get_recent_added()
        if len(list_bl) >= 1:
            self.subtotal = 0.00
            for item in list_bl:
                #self.subtotal += (item.item_amount * item.item_price)
                self.subtotal += item.total_price
            self.total = (self.subtotal * self.tax) + self.subtotal
        else:
            self.total = 0.00
            self.tax = 0.00
            self.subtotal = 0.00

    def clear_current_bill(self):
        self.ids.list_cur_bill.clear_added()
        self.update_preview()

    def _on_qrcode_dispatch(self):
        self.dispatch("on_scan_qrcode")

    def on_scan_qrcode(self, *args):
        toast(str(self.parent.parent))

    def _on_print_bill_dispatch(self):
        self.dispatch("on_print_bill")

    def on_print_bill(self, *args):
        toast(str(self.parent.parent))

    def _on_pay_dispatch(self):
        self.dispatch("on_paying")

    def on_paying(self, *args):
        toast(str(self.parent.parent))

    def check_table_Orders_exist_or_not(self):
        from kivymd.app import MDApp
        app = MDApp.get_running_app()

        if 'Orders' in app.local_sqlite.findTables():
            return
        else:
            from vietcuppos.local_database import SQLRawCommand
            conn = app.local_sqlite.connect_database()
            app.local_sqlite.create_table(
                SQLRawCommand.create_table_order,
                conn
            )

    def _on_save_curr_bill(self):
        cur_order = self.ids.list_cur_bill.get_recent_added()
        if not cur_order:
            toast("Nothings to Save")
            return
        else:
            import datetime
            import random
            self.check_table_Orders_exist_or_not()
            _dt = datetime.datetime.now()
            _code = "cs %d %d" % (len(
                    cur_order), random.randint(1, 999999))
            from kivymd.app import MDApp
            app = MDApp.get_running_app()
            # begin save current Order
            for order in cur_order:
                cur_order = (
                    _code,
                    order.item_name,
                    order.item_amount,
                    order.item_price,
                    "cashier",
                    '{}'.format(_dt)
                )
                conn = app.local_sqlite.connect_database()
                app.local_sqlite.insert_into_database(
                    "Orders", conn, cur_order)
            self.clear_current_bill()
            self.dispatch("on_save_curr_order")

    def on_save_curr_order(self, *args):
        pass
