from kivy.app import App
from kivy.lang import Builder
from kivy.event import EventDispatcher
from kivy.logger import Logger
from kivy.properties import AliasProperty, BooleanProperty, ColorProperty, ListProperty, ObjectProperty, DictProperty, OptionProperty
import os
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.utils import get_color_from_hex as ColorHex

from vietcuppos.font_definitions import theme_font_styles
from vietcuppos.color_definitions import colors, hue, palette
from vietcuppos.local_database import DatabaseSQLite


class Theme_Manger(EventDispatcher):

    bg_color = ListProperty([0, 0, 0])
    _bg_color_alp = ColorProperty([0, 0, 0, 0])
    _bg_color_noalp = ColorProperty([0, 0, 0, 0])
    light_color = ColorProperty([0, 0, 0, 0])
    dark_color = ColorProperty([0, 0, 0, 0])
    primary_color = ColorProperty([0, 0, 0, 0])
    text_color = ColorProperty([0, 0, 0, 0])
    disabled_text_color = ColorProperty([0.2, 0.2, 0.2, 1])

    font_styles = DictProperty(
        {
            "H1": ["Neusa VietCup", 96, False, -1.5],
            "H2": ["Neusa VietCup", 60, False, -0.5],
            "H3": ["FS GillSansMTPro VietCup", 48, False, 0],
            "H4": ["FS GillSansMTPro VietCup", 34, False, 0.25],
            "H5": ["FS GillSansMTPro VietCup", 24, False, 0],
            "H6": ["Roboto VietCup", 20, False, 0.15],
            "Subtitle1": ["FS GillSansMTPro VietCup", 16, False, 0.15],
            "Subtitle2": ["VDUFFY VietCup", 14, False, 0.1],
            "Body1": ["FS GillSansMTPro VietCup", 16, False, 0.5],
            "Body2": ["FS GillSansMTPro VietCup", 14, False, 0.25],
            "Button": ["VDUFFY VietCup", 14, True, 1.25],
            "Caption": ["FS GillSansMTPro VietCup", 12, False, 0.4],
            "Overline": ["FS GillSansMTPro VietCup", 10, True, 1.5],
            "Icon": ["Icons", 24, False, 0],
        }
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(font_styles=self.sync_theme_styles)
        self.colors = colors
        Clock.schedule_once(self.sync_theme_styles)

    def sync_theme_styles(self, *args):
        # Syncs the values from self.font_styles to theme_font_styles
        # this will ensure continuity when someone registers a new font_style.
        for num, style in enumerate(theme_font_styles):
            if style not in self.font_styles:
                theme_font_styles.pop(num)
        for style in self.font_styles.keys():
            theme_font_styles.append(style)

    def on_bg_color(self, *args):
        print(str(args))
        if len(self.bg_color) > 3:
            Logger.info(
                "bg_color alpha channel cannot be set. Ignoring provided alpha channel value"
            )
        self._bg_color_noalp = [self.bg_color[0],
                                self.bg_color[1], self.bg_color[2], 0]
        self._bg_color_alp = [self.bg_color[0],
                              self.bg_color[1], self.bg_color[2], 1]


class MainAppManager(ScreenManager):

    def __init__(self, **kwargs):
        super(MainAppManager, self).__init__(**kwargs)
        self.transition = NoTransition()


class POSApp(App):
    theme_manager = ObjectProperty()
    app_scrn_mgr = ObjectProperty()

    local_sqlite = ObjectProperty()

    theme_dialog = ObjectProperty()
    theme_cls = ObjectProperty()

    use_kivymd = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.theme_manager = Theme_Manger()
        self.app_scrn_mgr = MainAppManager()
        self.local_sqlite = DatabaseSQLite()

        self.KV_DIR = os.path.join(self.directory, "vietcuppos", "uix")
        self.load_all_kv_strings()

    def load_all_kv_strings(self):
        for d, dirs, files in os.walk(self.KV_DIR):
            for f in files:
                if os.path.splitext(f)[1] == ".kv":
                    path = os.path.join(d, f)
                    with open(path, encoding="utf-8") as kv_file:
                        Builder.load_string(kv_file.read())
    # use KivyMD or not

    def on_use_kivymd(self, *args):
        if self.use_kivymd:
            # Check to see if kivymd is installed
            try:
                import kivymd
            except ImportError:

                raise ImportError(
                    """Please install kivymd before using it in your application"""
                )
            from kivymd.theming import ThemeManager
            from kivymd.uix.picker import MDThemePicker
            self.theme_cls = ThemeManager()
            self.theme_dialog = MDThemePicker()
