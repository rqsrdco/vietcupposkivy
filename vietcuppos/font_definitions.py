from kivy.core.text import LabelBase

from vietcuppos import fonts_path

fonts = [
    {
        "name": "Neusa VietCup",
        "fn_regular": fonts_path + "Neusa Bold.otf",
        "fn_bold": fonts_path + "Neusa Bold.otf",
    },
    {
        "name": "FS GillSansMTPro VietCup",
        "fn_regular": fonts_path + "FS GillSansMTPro-Medium.ttf",
    },
    {
        "name": "Roboto VietCup",
        "fn_regular": fonts_path + "Roboto-Italic.ttf",
        "fn_italic": fonts_path + "Roboto-Italic.ttf",
    },
    {
        "name": "VDUFFY VietCup",
        "fn_regular": fonts_path + "vni.common.VDUFFY.ttf",
    },
    {
        "name": "Icons",
        "fn_regular": fonts_path + "materialdesignicons-webfont.ttf",
    },
]

for font in fonts:
    LabelBase.register(**font)

theme_font_styles = [
    "H1",
    "H2",
    "H3",
    "H4",
    "H5",
    "H6",
    "Subtitle1",
    "Subtitle2",
    "Body1",
    "Body2",
    "Button",
    "Caption",
    "Overline",
    "Icon",
]
