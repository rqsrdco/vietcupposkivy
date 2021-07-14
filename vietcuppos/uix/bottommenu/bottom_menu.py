from kivy.animation import Animation
from kivy.event import EventDispatcher
from kivy.properties import (
    BooleanProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    StringProperty,
)
from kivy.uix.relativelayout import RelativeLayout
from kivymd.theming import ThemableBehavior
from kivymd.uix.boxlayout import MDBoxLayout


class AdaptiveBox(MDBoxLayout):
    _root = ObjectProperty()


class BaseMenu(ThemableBehavior, AdaptiveBox):
    bg_color = ListProperty()
    _bg_color = ListProperty([0, 0, 0, 0])


class BottomMenuMainContent(AdaptiveBox):
    _root = ObjectProperty()


class BottomMenuTopContent(BaseMenu):
    pass


class BottomMenuBottomContent(BaseMenu):
    pass


class MenuBox(AdaptiveBox):
    _root = ObjectProperty()
    _first_touch_y = None
    _top_dis = None
    _allow_move = False
    _last_pos = None

    def on_touch_down(self, touch):
        pos = touch.pos
        if not self.collide_point(*pos):
            return False

        self._first_touch_y = pos[1]
        self._top_dis = self.top - self._first_touch_y
        self._last_pos = -(self.height - (self._top_dis + pos[1]))
        self._allow_move = True

        for child in self.children[:]:
            if child.dispatch("on_touch_down", touch):
                return True

        return True

    def on_touch_move(self, touch):
        pos = touch.pos
        if not self._root.allow_swipe:
            return False

        if not self.collide_point(*pos) and not self._allow_move:
            return False

        pos = touch.pos
        if not self._first_touch_y:
            return False

        distance = abs(pos[1] - self._first_touch_y)
        if distance < self._root.swipe_start_distance and not self._allow_move:
            return False

        self._allow_move = True
        showing_y = self._top_dis + pos[1]

        if showing_y < self._root._top_content.height:
            return False

        new_pos = -(self.height - showing_y)
        if new_pos >= 0:
            return False

        self.y = new_pos

    def on_touch_up(self, touch):
        pos = touch.pos
        self._allow_move = False

        if not self._root.allow_swipe:
            return False

        if not self._first_touch_y:
            return False

        if not self.collide_point(*pos):
            if self._root.auto_dismiss:
                self._dismiss()
            return False

        swipe_distance = pos[1] - self._first_touch_y
        if abs(swipe_distance) > self._root.swipe_distance:

            if swipe_distance > 0:
                self._open()
            elif swipe_distance < 0:
                self._dismiss()
        else:
            self._roll_back()

    def _open(self, *args):
        anim = Animation(y=0, d=self._root.duration, t=self._root.transition)
        anim.start(self)
        self._root.dispatch("on_open")
        self._root._status = "open"

    def _dismiss(self, *args):
        anim = Animation(
            top=self._root._top_content.height,
            d=self._root.duration,
            t=self._root.transition,
        )
        anim.start(self)
        self._root.dispatch("on_dismiss")
        self._root._status = "close"

    def _roll_back(self, *args):
        anim = Animation(
            y=self._last_pos, d=self._root.duration, t=self._root.transition
        )
        anim.start(self)


class BottomMenu(RelativeLayout, EventDispatcher):

    swipe_start_distance = NumericProperty("5dp")
    """
    Distance to move before any move happens.

    :attr:`swipe_start_distance` is a :class:`~kivy.properties.NumericProperty`
    and defaults to `'5dp'`.
    """

    swipe_distance = NumericProperty("40dp")
    """
    The minimum distance to be covered before the touch is considered a swipe gesture and Swiper gets closed/opened.

    :attr:`swipe_distance` is a :class:`~kivy.properties.NumericProperty`
    and defaults to `'40dp'`.
    """

    transition = StringProperty("out_quad")
    """
    The Animation transition type.

    :attr:`transition` is a :class:`~kivy.properties.StringProperty`
    and defaults to `'out_quad'`.
    """

    duration = NumericProperty(0.25)
    """
    The Animation transition duration in seconds.

    :attr:`duration` is a :class:`~kivy.properties.NumericProperty`
    and defaults to `0.25`.
    """

    auto_dismiss = BooleanProperty(True)
    """
    Determines if the view is automatically dismissed when the user clicks outside it.

    :attr:`auto_dismiss` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to `True`.
    """

    allow_swipe = BooleanProperty(True)
    """
    Enable/Disable swiping by touch.

    :attr:`allow_swipe` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to `True`.
    """

    _top_content = ObjectProperty()
    _bottom_content = ObjectProperty()
    _menu = ObjectProperty()
    _anim_playing = False
    _status = "close"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type("on_open")
        self.register_event_type("on_dismiss")

    def add_widget(self, widget, index=0, canvas=None):

        if issubclass(widget.__class__, BottomMenuTopContent):
            widget._root = self
            self.ids._top_content.add_widget(widget)
            return
        elif issubclass(widget.__class__, BottomMenuBottomContent):
            widget._root = self
            self.ids._bottom_content.add_widget(widget)
            return
        elif issubclass(widget.__class__, BottomMenuMainContent):
            widget._root = self
            self.ids._content.add_widget(widget)
            return
        else:
            return super().add_widget(widget, index=index, canvas=canvas)

    def on_touch_down(self, touch):
        super().on_touch_down(touch)

    def get_status(self):
        """Returns the status of swiper. Can be one of `open` or `close`. """

        return self._status

    def _allow_anim(self, *args):
        self._anim_playing = False

    def open(self):
        """Opens the menu."""

        self._menu._open()

    def dismiss(self):
        """Dismiss the menu."""

        self._menu._dismiss()

    def on_open(self, *args):
        pass

    def on_dismiss(self, *args):
        pass
