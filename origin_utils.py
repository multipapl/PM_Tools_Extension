import bpy
from mathutils import Vector, Matrix

def center_origin():
    """Центрує оріджин обєкта в центрі маси"""
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')


def center_bottom_origin():
    """
    Центрує оріджин обєкта по осях X, Y та в мінімальну точку по осі Z (без зміщення обєкта)
    для всіх вибраних обєктів.
    """
    selected_objects = bpy.context.selected_objects
    if not selected_objects:
        return
    
    for obj in selected_objects:
        if obj.type not in {'MESH', 'CURVE', 'SURFACE', 'FONT'}:
            continue
        
        # Отримуємо координати вершин bounding box у глобальному просторі
        bbox_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]

        # Визначаємо мінімальну та максимальну точки по осях
        min_x = min(corner[0] for corner in bbox_corners)
        max_x = max(corner[0] for corner in bbox_corners)
        min_y = min(corner[1] for corner in bbox_corners)
        max_y = max(corner[1] for corner in bbox_corners)
        min_z = min(corner[2] for corner in bbox_corners)

        # Обчислюємо новий центр оріджина в глобальних координатах
        new_origin = Vector(((min_x + max_x) / 2, (min_y + max_y) / 2, min_z))

        # Переводимо його у локальні координати
        new_origin_local = obj.matrix_world.inverted() @ new_origin

        # Зміщуємо геометрію, щоб оріджин опинився у правильному місці
        translation_matrix = Matrix.Translation(-new_origin_local)
        obj.data.transform(translation_matrix)

        # Встановлюємо нову позицію об'єкта у світі
        obj.matrix_world.translation = new_origin



