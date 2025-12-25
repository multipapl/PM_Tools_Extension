import bpy
import math

def convert_max_empties_to_cameras():
    selected_objects = bpy.context.selected_objects
    base_empties = [obj for obj in selected_objects if not obj.name.endswith(".Target") and obj.type == 'EMPTY']
    
    if not base_empties:
        return 0

    coll_name = "Converted_Cameras"
    if coll_name not in bpy.data.collections:
        cam_collection = bpy.data.collections.new(coll_name)
        bpy.context.scene.collection.children.link(cam_collection)
    else:
        cam_collection = bpy.data.collections[coll_name]

    created_count = 0
    
    for old_empty in base_empties:
        target_name = f"{old_empty.name}.Target"
        old_target = bpy.data.objects.get(target_name)
        
        if old_target:
            # 1. Отримуємо чисті координати
            cam_pos = old_empty.matrix_world.to_translation()
            target_pos = old_target.matrix_world.to_translation()

            # 2. Створюємо чистий таргет (просто щоб не залежати від імпорту)
            new_target = bpy.data.objects.new(f"P_Target_{old_empty.name}", None)
            new_target.empty_display_type = 'PLAIN_AXES'
            new_target.location = target_pos
            cam_collection.objects.link(new_target)

            # 3. Створюємо камеру
            cam_data = bpy.data.cameras.new(name=old_empty.name)
            cam_data.show_passepartout = True
            cam_data.passepartout_alpha = 1.0
            
            cam_obj = bpy.data.objects.new(f"P_Cam_{old_empty.name}", cam_data)
            cam_obj.location = cam_pos
            cam_collection.objects.link(cam_obj)

            # --- КОНСТРЕЙН 1: Стеження (Track To) ---
            tt = cam_obj.constraints.new(type='TRACK_TO')
            tt.target = new_target
            tt.track_axis = 'TRACK_NEGATIVE_Z'
            tt.up_axis = 'UP_Y'

            # --- КОНСТРЕЙН 2: Вирівнювання (Limit Rotation) ---
            # Цей констрейн "перекриває" нахил від Track To
            lr = cam_obj.constraints.new(type='LIMIT_ROTATION')
            lr.name = "P_ARCH_Vertical_Fix"
            lr.use_limit_x = True
            lr.min_x = math.radians(90)
            lr.max_x = math.radians(90)
            lr.use_limit_y = True
            lr.min_y = 0
            lr.max_y = 0
            lr.owner_space = 'WORLD'
            lr.influence = 1.0 # За замовчуванням камера ідеально рівна
            
            if created_count == 0:
                bpy.context.scene.camera = cam_obj
                
            created_count += 1
            
    return created_count