# Файл: arrange_utils.py
# Містить лише "чисту" логіку, без класів Blender.

def arrange_objects_logic(selected_objects, sort_method):
    """
    Основна логіка сортування та розстановки об'єктів.
    Повертає кортеж (булеве значення успіху, повідомлення для користувача).
    """
    if len(selected_objects) < 2:
        return (False, "Please select at least two objects")

    max_x_dimension = 0.0
    for obj in selected_objects:
        if obj.dimensions.x > max_x_dimension:
            max_x_dimension = obj.dimensions.x

    spacing = max_x_dimension
    if spacing == 0.0:
        return (False, "Could not determine object width. Operation cancelled.")

    if sort_method == 'POLYCOUNT':
        sort_key = lambda obj: len(obj.data.polygons) if obj.type == 'MESH' and obj.data else 0
    else:  # 'SIZE'
        sort_key = lambda obj: obj.dimensions.x * obj.dimensions.y * obj.dimensions.z

    sorted_objects = sorted(selected_objects, key=sort_key)

    for index, obj in enumerate(sorted_objects):
        obj.location.x = spacing * index
        obj.location.y = 0
        obj.location.z = 0

    return (True, f"Arranged {len(sorted_objects)} objects. Method: {sort_method.title()}.")