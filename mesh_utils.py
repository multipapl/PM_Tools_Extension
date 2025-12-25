import bpy

def link_instances_by_vertex_count():
    selected_objects = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
    
    if len(selected_objects) < 2:
        return {"CANCELLED"}

    # Словник для групування: {кількість_вертексів: [список_об'єктів]}
    groups = {}

    for obj in selected_objects:
        v_count = len(obj.data.vertices)
        if v_count not in groups:
            groups[v_count] = []
        groups[v_count].append(obj)

    linked_count = 0
    for v_count, obs in groups.items():
        if len(obs) > 1:
            # Беремо перший об'єкт як джерело даних (Master)
            master_data = obs[0].data
            for i in range(1, len(obs)):
                # Лінкуємо дані
                obs[i].data = master_data
                linked_count += 1
                
    return linked_count