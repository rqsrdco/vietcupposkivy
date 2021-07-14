from kivymd.uix.list import OneLineListItem
from kivymd.uix.card import MDCard
from kivy.properties import (
    NumericProperty,
    StringProperty,
    ObjectProperty,
    BooleanProperty,
)
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button


class NumberListItem(OneLineListItem):
    text = StringProperty()


class BillItem(MDCard):

    title = StringProperty()
    count = NumericProperty(1)
    price = StringProperty()
    drop_down = ObjectProperty()

    # def __init__(self, **kwargs):
    #    super().__init__(*kwargs)

    #    # self.init_dropdown()

    def init_dropdown(self):
        self.drop_down = DropDown()
        for index in range(15):
            # now, Add the button in the drop down list
            btton = Button(text='% d' % index, size_hint_y=None, height=30)

            # now we will bind the button for showing the text when it is selected
            btton.bind(
                on_release=lambda btton: self.drop_down.select(btton.text))

            # then we will add the button inside the drop_down list
            self.drop_down.add_widget(btton)

        self.ids.count.bind(on_release=self.drop_down.open)
        self.drop_down.bind(on_select=lambda instance,
                            x: setattr(self.ids.count, 'text', x))
