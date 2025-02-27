import bpy
import bmesh
from mathutils import Vector #papl

def create_lights_from_faces(obj, is_portal, visible_to_camera):
    """ 
    Створює Area Lights у центрі вибраних полігонів.
    
    :param obj: Активний об'єкт (меш)
    :param is_portal: Чи створювати портал-світильники
    :param visible_to_camera: Чи будуть світильники видимі у камері
    """
    bm = bmesh.from_edit_mesh(obj.data)
    selected_face_indices = [f.index for f in bm.faces if f.select]

    if not selected_face_indices:
        return "No faces selected"

    bpy.ops.object.mode_set(mode='OBJECT')

    depsgraph = bpy.context.evaluated_depsgraph_get()
    eval_obj = obj.evaluated_get(depsgraph)
    mesh = eval_obj.data

    for face_idx in selected_face_indices:
        if face_idx >= len(mesh.polygons):
            continue

        poly = mesh.polygons[face_idx]

        matrix = eval_obj.matrix_world
        center = matrix @ poly.center
        normal = (matrix.to_3x3().normalized() @ poly.normal).normalized()
        offset_distance = 0.0005
        center += normal * offset_distance

        verts = [matrix @ eval_obj.data.vertices[v].co for v in poly.vertices]
        rot_quat = normal.rotation_difference(Vector((0, 0, 1)))
        inv_rot = rot_quat.inverted()

        min_x = min_y = float('inf')
        max_x = max_y = -float('inf')

        for v in verts:
            local_pos = inv_rot @ (v - (center - normal * offset_distance))
            min_x = min(min_x, local_pos.x)
            max_x = max(max_x, local_pos.x)
            min_y = min(min_y, local_pos.y)
            max_y = max(max_y, local_pos.y)

        width = max_x - min_x
        height = max_y - min_y

        light_name = "Portal" if is_portal else "AreaLight"
        light_data = bpy.data.lights.new(name=light_name, type='AREA')
        light_obj = bpy.data.objects.new(name=light_name, object_data=light_data)
        bpy.context.collection.objects.link(light_obj)

        light_obj.location = center
        light_obj.rotation_mode = 'QUATERNION'

        if is_portal:
            light_obj.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(normal)
            light_data.cycles.is_portal = True
        else:
            light_obj.rotation_quaternion = Vector((0, 0, -1)).rotation_difference(normal)
            light_data.cycles.is_portal = False

        light_data.shape = 'RECTANGLE'
        light_data.size = width
        light_data.size_y = height
        light_obj.visible_camera = visible_to_camera

    bpy.ops.object.mode_set(mode='EDIT')
    return "Lights created successfully"
