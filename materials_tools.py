import bpy
import re

def cleanup_duplicates_in_selected_objects():
    pattern = re.compile(r"^(.*)\.(\d{3})$")
    replacements = {}

    selected_objects = [obj for obj in bpy.context.selected_objects if hasattr(obj.data, "materials")]

    for obj in selected_objects:
        for mat in obj.data.materials:
            if mat is None:
                continue
            match = pattern.match(mat.name)
            if match:
                base_name = match.group(1)
                if base_name in bpy.data.materials:
                    replacements[mat.name] = base_name

    if not replacements:
        return 0

    for obj in selected_objects:
        for i, mat in enumerate(obj.data.materials):
            if mat and mat.name in replacements:
                obj.data.materials[i] = bpy.data.materials[replacements[mat.name]]

    return len(replacements)
