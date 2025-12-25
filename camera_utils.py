import bpy

def convert_max_empties_to_cameras():
    selected_objects = bpy.context.selected_objects
    
    # Фільтруємо головні емпті (ті, що не є таргетами)
    base_empties = [obj for obj in selected_objects if not obj.name.endswith(".Target") and obj.type == 'EMPTY']
    
    created_count = 0
    
    for empty in base_empties:
        target_name = f"{empty.name}.Target"
        target_obj = bpy.data.objects.get(target_name)
        
        if target_obj:
            # Створюємо дані та об'єкт камери
            cam_data = bpy.data.cameras.new(name=empty.name)
            cam_obj = bpy.data.objects.new(empty.name + "_Cam", cam_data)
            bpy.context.collection.objects.link(cam_obj)
            
            # Копіюємо трансформи з головного емпті
            cam_obj.matrix_world = empty.matrix_world
            
            # Додаємо Track To констрейн
            tt = cam_obj.constraints.new(type='TRACK_TO')
            tt.target = target_obj
            tt.track_axis = 'TRACK_NEGATIVE_Z' # Стандарт для камер Blender
            tt.up_axis = 'UP_Y'
            
            created_count += 1
            
    return created_count