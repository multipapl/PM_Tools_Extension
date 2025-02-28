import bpy

def toggle_modifiers_by_name(modifier_name):
    """Вмикає/вимикає модифікатори з вказаною назвою у всіх об'єктах у сцені."""
    
    if not bpy.data.objects:
        return

    # Перевіряємо статус першого знайденого модифікатора з такою назвою
    current_state = None
    for obj in bpy.data.objects:
        for mod in obj.modifiers:
            if mod.name == modifier_name:
                current_state = mod.show_viewport
                break
        if current_state is not None:
            break

    if current_state is None:
        print(f"⚠️ Не знайдено модифікаторів із назвою '{modifier_name}'!")
        return
    
    # Інвертуємо стан модифікаторів
    new_state = not current_state
    for obj in bpy.data.objects:
        for mod in obj.modifiers:
            if mod.name == modifier_name:
                mod.show_viewport = new_state
                mod.show_render = new_state
                print(f'🔧 {obj.name}: {modifier_name} → Вюпорт: {mod.show_viewport}, Рендер: {mod.show_render}')
