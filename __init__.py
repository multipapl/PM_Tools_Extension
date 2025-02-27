""" import sys
import os

# Додаємо поточну директорію в sys.path для коректного імпорту
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Тепер імпорти будуть працювати

from . import panel, operators """

""" import bpy
from . import panel, operators """

import sys
import os

# Перевіряємо, чи ми працюємо в середовищі Blender
IN_BLENDER = "bpy" in sys.modules

if not IN_BLENDER:  # Якщо ми не в Blender (тобто в VS Code)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.append(current_dir)  # Додаємо шлях тільки для VS Code

# Імпортуємо модулі (відносні для Blender, абсолютні для VS Code)
try:
    from bl_ext.papl_tools import panel, operators  # Blender Extensions
except ImportError:
    from . import panel, operators  # Для тестування в VS Code


def register():
    panel.register()
    operators.register()

def unregister():
    operators.unregister()
    panel.unregister()

if __name__ == "__main__":
    register()