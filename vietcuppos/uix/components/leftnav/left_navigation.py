from kivy.animation import Animation
from kivy.clock import Clock
from kivy.properties import (
    BooleanProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    StringProperty,
)
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivymd.theming import ThemableBehavior


class LeftItemBase(BoxLayout):
    pass


class LeftLogoItem(LeftItemBase):
    pass


class LeftNavigationItem(ThemableBehavior, ButtonBehavior, LeftItemBase):
    icon = StringProperty()
    text = StringProperty()
    text_color = ListProperty([0, 0, 0, 0])
    icon_color = ListProperty([0, 0, 0, 0])
    active_text_color = ListProperty([0, 0, 0, 0])
    active_icon_color = ListProperty([0, 0, 0, 0])
    active = BooleanProperty(False)
    font_name = StringProperty("")
    _root = ObjectProperty()

    item_text_opacity = NumericProperty(1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(lambda x: self._update())

    def _update(self):

        if self.active_text_color == [0, 0, 0, 0]:
            self.active_text_color = self.theme_cls.accent_color

        if self.text_color == [0, 0, 0, 0]:
            self.text_color = self.theme_cls.text_color

        if self.active_icon_color == [0, 0, 0, 0]:
            self.active_icon_color = self.theme_cls.accent_color

        if self.icon_color == [0, 0, 0, 0]:
            self.icon_color = self.theme_cls.text_color

    def on_release(self):
        index = self._root.ids.items_box.children.index(self)
        self._root.set_current(index, item_index=False)
        return super().on_release()


class LeftNavigationContent(BoxLayout):
    pass


class LeftNavigation(ThemableBehavior, BoxLayout):
    opening_width = NumericProperty("200dp")
    navigation_bg_color = ListProperty()
    item_height = NumericProperty("52dp")
    item_radius = NumericProperty("68dp")
    active_color = ListProperty()
    transition = StringProperty("out_quad")
    duration = NumericProperty(0.2)

    _ghost_pos_y = NumericProperty(0)
    _selected = None
    _opening_width = NumericProperty()
    _item_radius = NumericProperty()
    _state = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(lambda x: self._update())
        self.register_event_type("on_open")
        self.register_event_type("on_dismiss")

    def _update(self):
        if not self.navigation_bg_color:
            self.navigation_bg_color = self.theme_cls.primary_color
        self._opening_width = self.opening_width
        self._item_radius = self.item_radius
        self.dismiss()

    def get_state(self):
        return self._state

    def on_dismiss(self, *args):
        pass

    def dismiss(self):
        width = self.item_height
        anim = Animation(
            _opening_width=width,
            _item_radius=width / 2,
            duration=self.duration,
            t=self.transition,
        )
        anim.start(self)
        self._hide_text()
        self.dispatch("on_dismiss")
        self._state = "dismiss"
        return

    def on_open(self, *args):
        pass

    def open(self):
        width = self.opening_width
        anim = Animation(
            _opening_width=width,
            _item_radius=self.item_radius,
            duration=self.duration,
            t=self.transition,
        )
        anim.start(self)
        self.dispatch("on_open")
        self._show_text()
        self._state = "open"
        return

    def _set_ghost_pos(self, y, anim):
        if anim:
            anim = Animation(
                _ghost_pos_y=y, t=self.transition, duration=self.duration
            )
            anim.start(self)
        else:
            self._ghost_pos_y = y
        return

    def refresh_items(self):
        if not self._selected:
            return
        Clock.schedule_once(
            lambda x: self.set_current(
                self._selected, item_index=False, anim=False
            )
        )
        return

    def set_current(self, index, item_index=True, anim=True):
        if item_index:
            item = self.get_item_children()[index]
            all_items = self.get_all_children()
            index = all_items.index(item)

        button = self.ids.items_box.children[index]
        y = button.pos[1]
        self._activete_button(button)
        self._set_selected(index)
        self._set_ghost_pos(y, anim=anim)

    def _activete_button(self, button):
        for item in self.get_item_children():
            item.active = False
        button.active = True
        return

    def get_item_children(self):
        children = [
            item
            for item in self.ids.items_box.children
            if issubclass(item.__class__, LeftNavigationItem)
        ]
        return children

    def get_all_children(self):
        return [item for item in self.ids.items_box.children]

    def _set_selected(self, index):
        self._selected = index

    def on_size(self, *args):
        self.refresh_items()

    def add_widget(self, widget, index=0, canvas=None):
        if issubclass(widget.__class__, LeftNavigationItem):
            self.ids.items_box.add_widget(widget)
            widget._root = self
            widget.bind(pos=lambda *args: self.set_current(-1, anim=False))
        elif issubclass(widget.__class__, LeftLogoItem):
            self.ids.items_box.add_widget(widget)

        elif issubclass(widget.__class__, LeftNavigationContent):
            self.ids.content.add_widget(widget)
        else:
            return super().add_widget(widget, index=index, canvas=canvas)

    def _hide_text(self):
        for item in self.get_item_children():
            anim = Animation(
                item_text_opacity=0,
                duration=self.duration / 2,
                t=self.transition,
            )
            anim.start(item)

    def _show_text(self):
        for item in self.get_item_children():
            anim = Animation(
                item_text_opacity=1,
                duration=self.duration / 2,
                t=self.transition,
            )
            anim.start(item)
