import bpy # type: ignore

def adjust_custom_distance():

    # Зберігаємо поточний рендер-движок
    current_engine = bpy.context.scene.render.engine

    # Визначаємо назву Eevee (у різних версіях Blender вона може бути різною)
    eevee_engine = "BLENDER_EEVEE_NEXT" if "BLENDER_EEVEE_NEXT" in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items else "BLENDER_EEVEE"

    # Переключаємо в Eevee, щоб був доступний параметр Custom Distance
    bpy.context.scene.render.engine = eevee_engine

    # Обробляємо всі вибрані світильники
    for obj in bpy.context.selected_objects:
        if obj.type == 'LIGHT':  # Перевіряємо, чи це світильник
            light = obj.data
            if hasattr(light, "use_custom_distance"):
                light.use_custom_distance = True  # Увімкнути параметр
                light.cutoff_distance /= 100  # Зменшуємо у 100 разів
                print(f"Updated custom distance for {obj.name}: {light.cutoff_distance}")

    # Повертаємо рендер-движок назад
    bpy.context.scene.render.engine = current_engine

    print("Custom Distance зменшено. Рендер повернено до попереднього значення.")
