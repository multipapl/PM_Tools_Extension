bl_info = {
    "name": "Papl Tools",
    "author": "Papl",
    "version": (1, 0, 95),  # Поточна версія
    "blender": (4, 2, 0),  # Мінімальна версія Blender для роботи
    "location": "View3D > Sidebar > Papl_Tools", # Де шукати аддон в інтерфейсі
    "description": "Короткий опис того, що робить аддон",
    "warning": "",
    "doc_url": "", # Посилання на документацію, якщо є
    "category": "Object", # Категорія в списку аддонів
}

import bpy
from . import panel, operators

def register():
    panel.register()
    operators.register()

def unregister():
    operators.unregister()
    panel.unregister()

if __name__ == "__main__":
    register()