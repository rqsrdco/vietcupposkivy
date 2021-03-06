from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.event import EventDispatcher
from kivy.metrics import dp
from kivy.properties import (
    BooleanProperty,
    ListProperty,
    NumericProperty,
    StringProperty,
)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.carousel import Carousel
from kivy.uix.widget import Widget
from kivymd.theming import ThemableBehavior
from kivy.utils import get_color_from_hex as ColorHex


class ItemCircles(ThemableBehavior, Widget):
    _circles_color = ListProperty(ColorHex("#F1E9C60F"))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class MyCarousel(ThemableBehavior, Carousel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(lambda x: self._add_circles())
        Window.bind(on_resize=self._on_resize)

    def _add_circles(self):
        self.total_circles = len(self.slides) - 1

        if self.parent.circles_color:
            circle_color = self.parent.circles_color
        else:
            circle_color = self.theme_cls.primary_color

        for _ in range(self.total_circles + 1):
            self.parent.ids.circles_box.add_widget(
                ItemCircles(
                    width=self.parent.circles_size, _circles_color=circle_color
                )
            )

        self._current_circle = self.total_circles
        Clock.schedule_once(
            lambda x: self._set_current_circle(animation=False))

    def on_size(self, *args):
        Clock.schedule_once(
            lambda x: self._set_current_circle(animation=False))
        return super().on_size(*args)

    def reset(self):
        self._current_circle = self.total_circles
        self._set_current_circle()
        self.load_slide(self.slides[0])

    def _set_current_circle(self, mode=None, animation=True):
        if mode == "next":
            if self._current_circle > 0:
                self._current_circle -= 1
            else:
                self.reset()

        elif mode == "previous":
            if self._current_circle < self.total_circles:
                self._current_circle += 1
        if animation:
            anim = Animation(
                pos=self.parent.ids.circles_box.children[
                    self._current_circle
                ].pos,
                t=self.anim_type,
                duration=self.anim_move_duration,
            )
            anim.start(self.parent.ids.ghost_circle)
        else:
            self.parent.ids.ghost_circle.pos = (
                self.parent.ids.circles_box.children[self._current_circle].pos
            )

    def on_touch_up(self, touch):
        if abs(self._offset) > self.width * self.min_move:

            if self._offset > 0:  # previous screen
                self._set_current_circle("previous")

            elif self._offset < 0:  # next screen
                self._set_current_circle("next")

        return super().on_touch_up(touch)

    def _on_resize(self, *args):
        Clock.schedule_once(
            lambda x: self._set_current_circle(animation=False))


class MenuItem(BoxLayout):
    pass


class MenuOperation(ThemableBehavior, BoxLayout, EventDispatcher):

    circles_size = NumericProperty(dp(20))
    skip_button = BooleanProperty(True)
    min_move = NumericProperty(0.05)
    anim_type = StringProperty("out_quad")
    anim_move_duration = NumericProperty(0.2)
    bottom_bar_radius = ListProperty([dp(20), dp(20), 0, 0])
    show_bottom_bar = BooleanProperty(True)
    bottom_bar_color = ListProperty(None)
    circles_color = ListProperty(ColorHex("#F1E9C6"))

    def __init__(self, **kwargs):
        super(MenuOperation, self).__init__(**kwargs)
        # self.register_event_type("on_finish")
        self.register_event_type("on_clear")
        self.register_event_type("on_select_all")
        self.register_event_type("on_ok")
        Clock.schedule_once(lambda x: self._update())

    def add_widget(self, widget, index=0, canvas=None):
        if issubclass(widget.__class__, MenuItem):
            self.ids.carousel.add_widget(widget)
        else:
            super().add_widget(widget, index=index, canvas=canvas)

    # on_clear

    def _on_clear_dispatch(self):
        self.dispatch("on_clear")

    def on_clear(self, *args):
        pass

    # on_select_all
    def _on_select_all_dispatch(self):
        self.dispatch("on_select_all")

    def on_select_all(self, *args):
        pass

    # on_ok
    def _on_ok_dispatch(self):
        self.dispatch("on_ok")

    def on_ok(self, *args):
        pass

    def reset(self):
        return self.ids.carousel.reset()

    def on_size(self, *args):
        self.ids.carousel.size = self.size

    def _update(self):
        self.ids.ghost_circle.size = [self.circles_size, self.circles_size]
