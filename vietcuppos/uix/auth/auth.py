import os
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
from kivymd.uix.textfield import MDTextField


Window.size = (1024, 768)
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
    from kivymd.uix.textfield import MDTextFieldRound

    def validate_account(self):
        if self.ids.email_field.text != "" and self.ids.pwds.pwd_field.text != "":
            app = MDApp.get_running_app()
            user = None
            try:
                conn = app.local_sqlite.connect_database()
                user = app.local_sqlite.search_from_database(
                    "Users", conn, "email", self.ids.email_field.text, order_by="id")[0]
                conn.close()
            except Exception:
                pass
            if user is None:
                self.ids.email_field.hint_text = '[color=#FF0000]Invalid Email[/color]'
            else:
                #pwd_chk = hashlib.sha256(pwd_chk.encode()).hexdigest()
                #self.ids.email_field.hint_text = ""
                #self.ids.pwds.hint_text = ""
                if self.ids.pwds.pwd_field.text == user[6]:
                    account_type = user[7]
                    # info.text = '[color=#00FF00]Logged In successfully!!![/color]'
                    if account_type == 'Administrator':
                        self.canvas.clear()
                        app.root.current = 'admin'
                    else:
                        self.canvas.clear()
                        app.app_scrn_mgr.current = 'cashier'
                else:
                    self.ids.pwds.pwd_field.hint_text = '[color=#FF0000]Invalid Password[/color]'
        else:
            if self.ids.email_field.text == "":
                self.ids.email_field.hint_text = "Email required"
            if self.ids.pwds.text == "":
                self.ids.pwds.pwd_field.hint_text = "Password required"
