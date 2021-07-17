from kivymd.uix.gridlayout import MDGridLayout
from kivymd.theming import ThemableBehavior

from kivy.properties import ObjectProperty, ListProperty, StringProperty, NumericProperty, DictProperty
from kivy.utils import get_color_from_hex as ColorHex
from kivy.event import EventDispatcher
from kivy.clock import Clock
from vietcuppos.uix.components import ListItemBill


class BillsOperation(ThemableBehavior, MDGridLayout, EventDispatcher):
    def __init__(self, **kwargs):
        super(BillsOperation, self).__init__(**kwargs)
        self.register_event_type("on_scan_qrcode")
        self.register_event_type("on_clear_current_bill")
        self.register_event_type("on_print_bill")
        self.register_event_type("on_paying")
        Clock.schedule_once(lambda x: self._update())

    def add_widget(self, widget):
        if issubclass(widget.__class__, ListItemBill):
            self.ids.scrv_cur_bill.add_widget(widget)
        else:
            super().add_widget(widget)

    def _on_qrcode_dispatch(self):
        self.dispatch("on_scan_qrcode")

    def on_scan_qrcode(self, *args):
        pass

    def _on_clear_bill_dispatch(self):
        self.dispatch("on_clear_current_bill")

    def on_clear_current_bill(self, *args):
        pass

    def _on_print_bill_dispatch(self):
        self.dispatch("on_print_bill")

    def on_print_bill(self, *args):
        pass

    def _on_pay_dispatch(self):
        self.dispatch("on_paying")

    def on_paying(self, *args):
        pass
