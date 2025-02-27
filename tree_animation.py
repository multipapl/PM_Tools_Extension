import bpy

def create_tree_animation():
    """Створює анімацію хитання дерева та руху листя"""
    
    # Отримуємо активний об'єкт (меш дерева або листя)
    obj = bpy.context.object
    if not obj or obj.type != 'MESH':
        print("❌ Виберіть об'єкт типу MESH!")
        return

    # Генеруємо унікальні імена для Empty на основі назви меша
    empty_wind_name = f"{obj.name}_Empty_Wind"
    displace_name = "Leaf_Displace"
    bend_y_name = "Tree_Bend_Y"
    bend_x_name = "Tree_Bend_X"

    # =============== 1. Створення порожнього об'єкта для руху листочків ===============
    if empty_wind_name not in bpy.data.objects:
        empty_wind = bpy.data.objects.new(empty_wind_name, None)
        bpy.context.collection.objects.link(empty_wind)
        empty_wind.location = obj.location  # Розміщуємо біля дерева
        empty_wind.parent = obj  # Робимо меш батьком
        empty_wind.empty_display_size = 0.2
        empty_wind.empty_display_type = 'SPHERE'
    else:
        empty_wind = bpy.data.objects[empty_wind_name]

    # =============== 2. Додаємо драйвери для Empty (X та Z оберт) ===============
    drivers = [
        (empty_wind.driver_add("rotation_euler", 0), "frame / 300"),  # X оберт
        (empty_wind.driver_add("rotation_euler", 2), "frame / 200"),  # Z оберт
    ]

    for driver, expression in drivers:
        driver.driver.type = 'SCRIPTED'
        driver.driver.expression = expression

    # =============== 3. Додаємо Displace (рух листя) ===============
    if displace_name not in obj.modifiers:
        displace = obj.modifiers.new(displace_name, 'DISPLACE')

        # Перевіряємо, чи існує текстура "Wind_Texture"
        texture = bpy.data.textures.get("Wind_Texture")
    
        if not texture:  # Якщо такої текстури немає, створюємо нову
            texture = bpy.data.textures.new("Wind_Texture", 'CLOUDS')
            texture.noise_basis = 'IMPROVED_PERLIN'  # Використовуємо Improved Perlin

        displace.texture = texture
        displace.strength = 0.15  # Збільшена сила Displace
        displace.direction = 'NORMAL'
        displace.vertex_group = "VG_Leaves"
        displace.texture_coords = 'OBJECT'
        displace.texture_coords_object = empty_wind


    # =============== 4. Додаємо Simple Deform (Bend) для гнучкості дерева (по Y) ===============
    if bend_y_name not in obj.modifiers:
        bend_y = obj.modifiers.new(bend_y_name, 'SIMPLE_DEFORM')
        bend_y.deform_method = 'BEND'
        bend_y.origin = empty_wind  # Використовуємо Empty як Origin
        bend_y.angle = 0.0  # Початкове значення кута
        bend_y.vertex_group = "VG_Global"
        bend_y.deform_axis = 'Y'  # Згин по Y

        # Створюємо пустий ключовий кадр для кута Bend
        obj.animation_data_create()
        obj.animation_data.action = bpy.data.actions.new(name=f"{obj.name}_Bend_Action_Y")
        fcurve_bend_y = obj.animation_data.action.fcurves.new(f'modifiers["{bend_y_name}"].angle')
        fcurve_bend_y.keyframe_points.insert(0, 0)

        # Додаємо Generator (Coefficient = 0.1, x^1 = 0)
        generator_y = fcurve_bend_y.modifiers.new(type='GENERATOR')
        generator_y.mode = 'POLYNOMIAL'
        generator_y.coefficients = (0.1, 0.0)

        # Додаємо Noise (Scale = 80, Strength = 0.12)
        noise_bend_y = fcurve_bend_y.modifiers.new(type='NOISE')
        noise_bend_y.scale = 80
        noise_bend_y.strength = 0.12

    # =============== 5. Додаємо Simple Deform (Bend) для гнучкості дерева (по X) ===============
    if bend_x_name not in obj.modifiers:
        bend_x = obj.modifiers.new(bend_x_name, 'SIMPLE_DEFORM')
        bend_x.deform_method = 'BEND'
        bend_x.origin = empty_wind  # Використовуємо Empty як Origin
        bend_x.angle = 0.0  # Початкове значення кута
        bend_x.vertex_group = "VG_Global"
        bend_x.deform_axis = 'X'  # Згин по X

        # Створюємо пустий ключовий кадр для кута Bend
        fcurve_bend_x = obj.animation_data.action.fcurves.new(f'modifiers["{bend_x_name}"].angle')
        fcurve_bend_x.keyframe_points.insert(0, 0)

        # Додаємо Generator (Coefficient = 0.1, x^1 = 0)
        generator_x = fcurve_bend_x.modifiers.new(type='GENERATOR')
        generator_x.mode = 'POLYNOMIAL'
        generator_x.coefficients = (0.1, 0.0)

        # Додаємо Noise (Scale = 80, Strength = 0.12)
        noise_bend_x = fcurve_bend_x.modifiers.new(type='NOISE')
        noise_bend_x.scale = 80
        noise_bend_x.strength = 0.12
