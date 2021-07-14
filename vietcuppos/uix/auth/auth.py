from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.screen import MDScreen
from kivymd.theming import ThemableBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp

from kivy.properties import NumericProperty, StringProperty
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.lang import Builder

import os


Window.size = (700, 500)
Window.minimum_width, Window.minimum_height = Window.size


class LoginScreen(ThemableBehavior, MDScreen):

    scale_box_1 = NumericProperty(1)
    scale_box_2 = NumericProperty(1)
    card_x = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("---|LoginScreen| --- |__init__|---")

        self.name = 'auth'
        self.ids.enter_get_pass_btn.disabled = False
        self.ids.enter_signin_btn.disabled = True

    def on_pre_enter(self):
        print("---|LoginScreen| --- |on_pre_enter|---")

    def on_enter(self):
        print("---|LoginScreen| --- |on_enter|---")

    def on_size(self, *args):
        if self.card_x:
            self.card_x = self.ids.box.width - self.ids.box2.width - dp(40)

    def animation_to_right(self):
        def animation_complete(*args):
            self.ids.box2.add_widget(ForgetpPasswordBox())
            Animation(scale=1, d=0.1).start(self.ids.box2.children[0])

        self.ids.box2.clear_widgets()
        Animation(scale=1, d=0.3).start(self.ids.forgetpass_enabled_box)
        Animation(scale=0, d=0.3).start(self.ids.start_forgetpass_box)
        animation = Animation(
            card_x=self.ids.box.width - self.ids.box2.width - dp(40),
            d=0.3,
            t="in_out_cubic",
        )
        animation.bind(on_complete=animation_complete)
        animation.start(self)
        self.ids.enter_get_pass_btn.disabled = True
        self.ids.enter_signin_btn.disabled = False

    def animation_to_left(self):
        def animation_complete(*args):
            self.ids.box2.add_widget(SignInBox())
            Animation(scale=1, d=0.1).start(self.ids.box2.children[0])

        self.ids.box2.clear_widgets()
        Animation(scale=0, d=0.3).start(self.ids.forgetpass_enabled_box)
        Animation(scale=1, d=0.3).start(self.ids.start_forgetpass_box)
        animation = Animation(
            card_x=0,
            d=0.3,
            t="in_out_cubic",
        )
        animation.bind(on_complete=animation_complete)
        animation.start(self)
        self.ids.enter_get_pass_btn.disabled = False
        self.ids.enter_signin_btn.disabled = True


class ScaleBox(MDBoxLayout):
    scale = NumericProperty(1)


class ForgetpPasswordBox(ScaleBox):
    pass


class SignInBox(ScaleBox):
    pass


class ClickableTextFieldRound(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()
