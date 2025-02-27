import bpy
import random

def apply_random_offset():
    """Додає випадковий офсет до драйверів анімації ТІЛЬКИ для вибраних об'єктів"""
    
    # Визначення діапазону випадкового офсету
    min_offset = -500.0  # Мінімальний офсет кадру
    max_offset = 500.0   # Максимальний офсет кадру

    selected_objects = bpy.context.selected_objects

    if not selected_objects:
        print("⚠ Немає вибраних об'єктів для офсету!")
        return

    modified_objects = 0  # Лічильник змінених об'єктів

    # Проходження по кожному виділеному об'єкту
    for obj in selected_objects:
        if obj.animation_data and obj.animation_data.drivers:
            for driver in obj.animation_data.drivers:
                if "frame" in driver.driver.expression:  # Шукаємо драйвери, що використовують `frame`
                    random_offset = random.uniform(min_offset, max_offset)
                    new_expression = driver.driver.expression.replace("frame", f"(frame + {random_offset})")
                    driver.driver.expression = new_expression  # Оновлюємо вираз
                    modified_objects += 1

    # Оновлення вікна анімації
    bpy.context.area.tag_redraw()

    if modified_objects > 0:
        print(f"✅ Випадковий офсет додано до {modified_objects} об'єктів.")
    else:
        print("⚠ Жоден вибраний об'єкт не містить драйверів із 'frame'.")
