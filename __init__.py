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