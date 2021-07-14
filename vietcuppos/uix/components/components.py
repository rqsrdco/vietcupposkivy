from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ObjectProperty, StringProperty, ColorProperty, NumericProperty
from kivymd.uix.button import MDIconButton
from kivymd.theming import ThemableBehavior


class PasswordFieldRec(MDRelativeLayout):
    pwd_field = ObjectProperty()


class PasswordFieldRound(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()


class ItemBill(MDBoxLayout, ThemableBehavior):
    item_color = ColorProperty([1, 1, 1, 1])
    item_name = StringProperty()
    item_count = NumericProperty(1)
    item_price = NumericProperty(19000.99)

    def minus_item_count(self):
        if self.item_count > 1:
            self.item_count -= 1
        else:
            pass

    def plus_item_count(self):
        self.item_count += 1
