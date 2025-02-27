import bpy

def replace_meshes_with_instance():
    # Перевіряємо, чи є активний об'єкт і чи він є інстансом колекції
    active_obj = bpy.context.view_layer.objects.active
    if not active_obj or active_obj.instance_collection is None:
        print("Активний об'єкт має бути інстансом колекції.")
        return

    # Зберігаємо посилання на активний об'єкт і його інстанс-колекцію
    instance_collection = active_obj.instance_collection

    # Отримуємо список обраних об'єктів, виключаючи активний
    selected_objects = [obj for obj in bpy.context.selected_objects if obj != active_obj]

    for obj in selected_objects:
        if obj.type == 'MESH':
            # Зберігаємо позицію, обертання та масштаб меша
            location = obj.location
            rotation = obj.rotation_euler
            scale = obj.scale

            # Зберігаємо колекції, до яких належить об'єкт
            original_collections = obj.users_collection[:]

            # Створюємо новий інстанс колекції перед видаленням
            new_instance = bpy.data.objects.new(obj.name, None)
            new_instance.instance_type = 'COLLECTION'
            new_instance.instance_collection = instance_collection

            # Встановлюємо позицію, обертання та масштаб для інстанса
            new_instance.location = location
            new_instance.rotation_euler = rotation
            new_instance.scale = scale

            # Додаємо інстанс у всі ті ж колекції, де був оригінальний меш
            for col in original_collections:
                col.objects.link(new_instance)

            # Видаляємо оригінальний меш після створення інстанса
            if obj.name in bpy.data.objects:
                bpy.data.objects.remove(obj, do_unlink=True)

    # Оновлюємо контекст, щоб уникнути можливих проблем із скасуванням (undo)
    bpy.context.view_layer.update()