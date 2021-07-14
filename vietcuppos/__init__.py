import kivy
import os
print("__init__.py")

__version__ = "1.0.0"
"""VietCupPOS version."""

kivy.require("2.0.0")

path = os.path.dirname(__file__)
print("vietcuppos Package ", path)

fonts_path = os.path.join(path, f"fonts{os.sep}")
"""Path to fonts directory."""

images_path = os.path.join(path, f"images{os.sep}")
"""Path to images directory."""


import vietcuppos.factory_registers  # NOQA

import vietcuppos.font_definitions  # NOQA
