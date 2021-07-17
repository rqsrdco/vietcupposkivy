from kivymd.uix.behaviors import CircularRippleBehavior
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import IRightBodyTouch
from kivymd.theming import ThemableBehavior
from kivymd.uix.button import MDIconButton
from kivymd.uix.list import ILeftBody
from kivymd.uix.card import MDCard
from kivymd.uix.list import MDList
from kivymd.app import MDApp

from kivy.properties import ObjectProperty, StringProperty, ColorProperty, NumericProperty, BooleanProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.event import EventDispatcher
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.clock import Clock

import sys
import math
from decimal import Decimal


class LeftWidget(ILeftBody, Widget):
    pass


class PasswordFieldRec(MDRelativeLayout):
    pwd_field = ObjectProperty()


class PasswordFieldRound(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()


class Container(IRightBodyTouch, MDBoxLayout):
    adaptive_width = True


class ItemBill(MDCard, EventDispatcher):
    item_name = StringProperty()
    item_amount = NumericProperty(1)
    item_price = NumericProperty(19789.99)
    total_price = NumericProperty(0.0)

    def __init__(self, **kwargs):
        super(ItemBill, self).__init__(**kwargs)
        self.register_event_type("on_delete")
        Clock.schedule_once(lambda x: self._update())

    def _on_delete_dispatch(self):
        self.dispatch("on_delete")

    def on_delete(self, *args):
        pass

    def _update(self):
        self.total_price = (
            self.item_price * self.item_amount).quantize(Decimal('0.01'))

    def foobar(x): return x*(10**2)

    def minus_item_amount(self):
        if self.item_amount > 1:
            self.item_amount -= 1

    def plus_item_amount(self):
        self.item_amount += 1

    def on_item_amount(self, obj, value):
        self.total_price = self.foobar(self.item_price * value)

    # def on_event_delete(self, obj):
    #    print(obj)
    #    MDApp.get_running_app(
    #    ).root.current_screen.ids.left_navigation_contents.children[0].current_screen.remove_item_bill(self)

    def on_property(self, obj, value):
        print("Typical property change from", obj, "to", value)

    def on_anything(self, *args, **kwargs):
        print('The flexible function has *args of', str(args),
              "and **kwargs of", str(kwargs))


class ListItemBill(MDList):
    _added_list = []

    def get_recent_added(self):
        return self._added_list

    def clear_added(self):
        if not self._added_list:
            return
        self._added_list = []


class ItemMenu(ThemableBehavior, ButtonBehavior, CircularRippleBehavior, BoxLayout):
    columns = NumericProperty(4)
    source = StringProperty("")
    first_label = StringProperty("")
    second_label = StringProperty("")
    animate_start = BooleanProperty(True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _choose_selection(self, name, price):

        selected_dict = self.parent._selected_dict

        if selected_dict.get(name) is None:
            selected_dict["%s" % name] = price
            self._selection_anim()
        else:
            selected_dict.pop(name)
            self._deselection_anim()

        if not selected_dict:
            selected_dict = {}

        self.parent._selected_dict = selected_dict

    def _selection_anim(self):
        anim = Animation(font_size=self.width / 3,
                         t="out_bounce", duration=0.1)
        anim.start(self.ids._box)

    def _deselection_anim(self):
        anim = Animation(
            font_size=0,
            size=self.ids._box.texture_size,
            t="in_bounce",
            duration=0.1,
        )
        anim.start(self.ids._box)


class ListItemMenu(StackLayout):
    _selected_dict = {}

    def get_selection(self):
        return self._selected_dict

    def clear_selection(self):
        if not self.children:
            return

        for child in self.children:
            if child.first_label in self._selected_dict.keys():
                child._deselection_anim()
        self._selected_dict = {}

    def select_all(self):
        for child in self.children:
            if child.first_label not in self._selected_dict.keys():
                child._selection_anim()
                self._selected_dict["%s" %
                                    child.first_label] = child.second_label