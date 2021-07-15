from kivy.uix.boxlayout import BoxLayout
from kivymd.theming import ThemableBehavior
from kivy.uix.behaviors import ButtonBehavior

from kivy.properties import (
    BooleanProperty,
    ListProperty,
    NumericProperty,
    OptionProperty,
    StringProperty,
)
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.metrics import dp, sp


class BottomNavigation(ThemableBehavior, BoxLayout):
    """
    Class of the Navigation Bar 2
    """

    bottomnavigation_height = NumericProperty("65dp")
    """
    Height of the navigation bar

    :attr:`bottomnavigation_height` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `65dp`.
    """

    radius = NumericProperty("20dp")
    """
    Radius of the top corners of the navigation bar.

    :attr:`radius` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `20dp`.
    """

    bg_color = ListProperty(None)
    """
    Color of the navigation bar.

    :attr:`bg_color` is an :class:`~kivy.properties.ListProperty`
    and defaults to `'app.theme_cls.bg_darkest'`.
    """

    elelevation = NumericProperty(None)
    """
    Elevation of the navigation bar.

    :attr:`elevation` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `None`.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_resize=self._update)
        Clock.schedule_once(lambda x: self.set_current(None))
        Clock.schedule_once(lambda x: self._update())

    def _update(self, *args):
        self.width = Window.width
        buttons = self.ids._button_box.children
        button_sizes = (
            (len(buttons) - 1) * buttons[0].button_height
        ) + buttons[0].button_width
        space = self.width - button_sizes
        spacing = space / (len(buttons) + 1)
        self.ids._button_box.spacing = spacing
        self.ids._button_box.padding = [spacing, 0, spacing, 0]

    def set_current(self, index):
        """
        Call this method to set the Navigation bar to the icon with the passed `index`. If wrong
        index value is passed the first button(on left side) is selected.

        .. note:: The index starts from 0 till 1 minus total icons in the Navigation Bar. Index value starts
            from icons on right side of the screen
        """

        if not index:
            index = -1
        button = self.ids._button_box.children[index]
        button.dispatch("on_release")

    def add_widget(self, widget, index=0, canvas=None):
        if issubclass(widget.__class__, Button_Item):
            return self.ids._button_box.add_widget(widget)
        else:
            return super().add_widget(widget, index=index, canvas=canvas)


class Button_Item(ThemableBehavior, ButtonBehavior, BoxLayout):
    """
    This class represents an icon/button of the navigation bar
    """

    text = StringProperty()
    """
    Text to be placed inside button element

    :attr:`text` is an :class:`~kivy.properties.StringProperty`
    and defaults to `None`.
    """

    icon = StringProperty()
    """
    Icon to be placed inside the button element

    :attr:`icon` is an :class:`~kivy.properties.StringProperty`
    and defaults to `None`.
    """

    transition = StringProperty("out_quad")
    """
    The animation interpolation type to use for the selection animation of this icon/element.
    See `kivy transition interpolations <https://kivy.org/doc/stable/api-kivy.animation.html#kivy.animation.AnimationTransition>`_
    for all available options

    :attr:`transition` is an :class:`~kivy.properties.StringProperty`
    and defaults to `'out_quad'`.
    """

    duration = NumericProperty(0.3)
    """
    Duration of the selection animation

    :attr:`duration` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `0.3`.
    """

    button_bg_color = ListProperty(None)
    """
    Background color of the button.

    :attr:`button_bg_color` is an :class:`~kivy.properties.ListProperty`
    and defaults to `'app.theme_cls.primary_light'`.
    """

    button_width = NumericProperty(dp(120))
    """
    Width of the button.

    :attr:`button_width` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `120dp`.
    """

    button_height = NumericProperty(dp(40))
    """
    Height of the button.

    :attr:`button_height` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `40dp`.
    """

    text_size = NumericProperty(sp(13))
    """
    Size of text inside of button element.

    :attr:`text_size` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `13dp`.
    """

    text_color = ListProperty(None)
    """
    Color of text of the button.

    :attr:`text_color` is an :class:`~kivy.properties.ListProperty`
    and defaults to `'app.theme_cls.primary_dark'`.
    """

    icon_size = NumericProperty(dp(20))
    """
    Size of icon inside button element

    :attr:`icon_size` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `20dp`.
    """

    icon_color = ListProperty(None)
    """
    Color of the icon inside button element

    :attr:`icon_color` is an :class:`~kivy.properties.ListProperty`
    and defaults to `'app.theme_cls.primary_dark'`.
    """

    mode = OptionProperty(
        "color_on_normal", options=["color_on_normal", "color_on_active"]
    )
    """
    Sets the button element mode. Can be set to `color_on_normal` which means the `button_bg_color`
    will be shown even if the button is not selected in the navigation bar.
    Can also be set to `color_on_active` which means the button `button_bg_color` will only be
    shown when the button is selected im the navigation bar.

    :attr:`mode` is an :class:`~kivy.properties.OptionProperty`
    and defaults to `'color_on_normal'`.
    """
    # ================
    """
    .. rubric:: The following properties deal with the badges displayed on the button element
    """

    badge_bg_color = ListProperty()
    """
    Color of the bakground around a badge.

    :attr:`badge_bg_color` is an :class:`~kivy.properties.ListProperty`
    and defaults to `'app.theme_cls.bg_normal'`.
    """

    badgeitem_padding = NumericProperty(dp(3))
    """
    Padding for the badge.

    :attr:`badgeitem_padding` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `'3dp'`.
    """

    badgeitem_color = ListProperty()
    """
    Color of the badge.

    :attr:`badgeitem_color` is an :class:`~kivy.properties.ListProperty`
    and defaults to `'app.theme_cls.accent_color'`.
    """

    badge_position = StringProperty("right")
    """
    Position of the badge relative to the button it is on.
    Can be set to `right` or `left`.

    :attr:`badge_position` is an :class:`~kivy.properties.OptionProperty`
    and defaults to `'right'`.
    """

    badge_text = StringProperty("")
    """
    Text to be placed inside the badge.

    :attr:`badge_text` is an :class:`~kivy.properties.StringProperty`
    and defaults to `''`.
    """

    badge_bold = BooleanProperty(False)
    """
    Should the text inside the badge be bold

    :attr:`badge_bold` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    """

    badge_offset = NumericProperty(0.4)
    """
    Offset of the badge's center point from the corner of the widget it is applied to

    :attr:`badge_offset` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `0.4`.
    """
    badge_disabled = BooleanProperty(False)
    """
    Show the badge or not. If set to `False` the badge opacity will be set to 0.

    :attr:`badge_disabled` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    """

    _bg_opacity = NumericProperty(1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_release(self):
        for button in self.parent.children:
            if button == self:
                continue
            button._button_shrink()

        self._button_expand()
        return super().on_release()

    def _button_expand(self):
        label_anim = Animation(
            opacity=1, transition=self.transition, duration=self.duration
        )
        label_anim.start(self.ids._label)

        anim = Animation(
            width=self.button_width,
            _bg_opacity=1,
            t=self.transition,
            duration=self.duration,
        )
        anim.start(self)

    def _button_shrink(self):
        if self.mode == "color_on_active":
            opacity = 0
        else:
            opacity = 1

        label_anim = Animation(
            opacity=0, transition=self.transition, duration=self.duration
        )
        label_anim.start(self.ids._label)

        but_anim = Animation(
            width=self.height,
            _bg_opacity=opacity,
            t=self.transition,
            duration=self.duration,
        )
        but_anim.start(self)


class BadgeContent(BoxLayout):
    pass


class BadgeItem(ThemableBehavior, BoxLayout):
    bg_color = ListProperty()
    badgeitem_padding = NumericProperty()
    badgeitem_color = ListProperty()
    position = OptionProperty("right", options=["right", "left"])
    text = StringProperty("")
    bold = BooleanProperty()
    offset = NumericProperty()
    badge_disabled = BooleanProperty(False)


class BadgeLayout(FloatLayout):
    bg_color = ListProperty()
    """
    Color of the bakground around a badge.

    :attr:`bg_color` is an :class:`~kivy.properties.ListProperty`
    and defaults to `'app.theme_cls.bg_normal'`.
    """

    badgeitem_padding = NumericProperty(dp(3))
    """
    Padding for the badge.

    :attr:`badgeitem_padding` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `'3dp'`.
    """

    badgeitem_color = ListProperty()
    """
    Color of the badge.

    :attr:`badgeitem_color` is an :class:`~kivy.properties.ListProperty`
    and defaults to `'app.theme_cls.accent_color'`.
    """

    position = OptionProperty("right", options=["right", "left"])
    """
    Position of the badge relative to the widget it is on.
    Can be set to `right` or `left`.

    :attr:`position` is an :class:`~kivy.properties.OptionProperty`
    and defaults to `'right'`.
    """

    text = StringProperty("")
    """
    Text to be placed inside the badge.

    :attr:`text` is an :class:`~kivy.properties.StringProperty`
    and defaults to `''`.
    """

    bold = BooleanProperty(False)
    """
    Should the text inside the badge be bold

    :attr:`bold` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    """

    offset = NumericProperty(0.25)
    """
    Offset of the badge's center point from the corner of the widget it is applied to

    :attr:`offset` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `'0.25'`.
    """

    badge_disabled = BooleanProperty(False)
    """
    Show the badge or not. If set to `False` the badge opacity will be set to 0.

    :attr:`badge_disabled` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    """

    def add_widget(self, widget, index=0, canvas=None):
        if issubclass(widget.__class__, BadgeItem) or issubclass(
            widget.__class__, BadgeContent
        ):
            return super().add_widget(widget, index=index, canvas=canvas)
        else:
            return self.ids.box.add_widget(widget)
