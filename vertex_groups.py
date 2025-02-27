import bpy
import bmesh
import mathutils

def create_tree_vertex_groups():
    """Створює вертекс-групи для анімації дерев: VG_Leaves та VG_Global"""
    
    # Назви вертекс-груп
    leaf_group_name = "VG_Leaves"
    global_group_name = "VG_Global"

    # Ключові слова для пошуку в назвах матеріалів
    leaf_keywords = ["leaf", "leaves"]

    # Функція отримання UV-координати вершини
    def get_uv_for_vertex(obj, bm, uv_layer, vert):
        """Отримує середню UV-координату для вершини."""
        uvs = []
        for loop in vert.link_loops:
            if loop[uv_layer]:  # Перевіряємо, чи є UV
                uvs.append(loop[uv_layer].uv)
        if uvs:
            return sum(uvs, mathutils.Vector((0, 0))) / len(uvs)  # Середнє значення
        return None

    # Функція отримання мінімального та максимального Z-значення об'єкта
    def get_object_z_bounds(obj):
        min_z, max_z = float('inf'), float('-inf')
        depsgraph = bpy.context.evaluated_depsgraph_get()
        obj_eval = obj.evaluated_get(depsgraph)
        mesh = obj_eval.to_mesh()

        for v in mesh.vertices:
            world_v = obj.matrix_world @ v.co
            min_z = min(min_z, world_v.z)
            max_z = max(max_z, world_v.z)

        obj_eval.to_mesh_clear()
        return min_z, max_z

    # Проходження по всіх вибраних об'єктах
    for obj in bpy.context.selected_objects:
        if obj.type != 'MESH':
            continue  # Пропускаємо не-мешеві об'єкти

        # Отримуємо або створюємо вертекс-групи
        vg_leaves = obj.vertex_groups.get(leaf_group_name) or obj.vertex_groups.new(name=leaf_group_name)
        vg_global = obj.vertex_groups.get(global_group_name) or obj.vertex_groups.new(name=global_group_name)

        # Отримуємо межі по Z
        min_z, max_z = get_object_z_bounds(obj)

        # Переходимо в Edit Mode
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')

        # Створюємо BMesh для роботи з геометрією
        bm = bmesh.from_edit_mesh(obj.data)

        # Отримуємо UV-шари
        uv_layer = bm.loops.layers.uv.active
        if not uv_layer:
            print(f"⚠ У об'єкта {obj.name} немає UV-мапи! Пропускаємо...")
            bpy.ops.object.mode_set(mode='OBJECT')
            continue  # Пропускаємо об'єкт

        # Створюємо тимчасові списки для вершин
        leaves_vertices = []
        global_vertices = []

        # Отримуємо матеріали об'єкта
        materials = obj.data.materials

        # Обробка всіх граней та вершин
        for f in bm.faces:
            if f.material_index < len(materials):
                mat_name = materials[f.material_index].name.lower()

                # Листя (градієнт на основі V-координати UV)
                if any(keyword in mat_name for keyword in leaf_keywords):
                    for v in f.verts:
                        uv = get_uv_for_vertex(obj, bm, uv_layer, v)
                        if uv:  # Якщо вдалося отримати UV
                            weight = uv.y  # Використовуємо V-координату як градієнт

                            # Покращений градієнт: 80% листка червоні, останні 20% з градієнтом
                            if weight > 0.2:
                                weight = 1.0  # Верхня частина листка червона
                            else:
                                weight = weight / 0.2  # Плавний перехід в останній 1/5 листка

                            weight = max(0.0, min(1.0, weight))  # Обмежуємо значення
                            leaves_vertices.append((v.index, weight))

        # Глобальна градієнтна група (від 0 внизу до 1 вгорі)
        for v in bm.verts:
            world_v = obj.matrix_world @ v.co
            v_z_norm = (world_v.z - min_z) / (max_z - min_z)  # Нормалізуємо висоту

            # Покращений градієнт: верхні 2/3 - червоні, нижня 1/3 - градієнт
            if v_z_norm > 1/3:
                weight = 1.0  # Верх дерева червоний
            else:
                weight = v_z_norm * 3  # Плавний перехід у нижній третині

            weight = max(0.0, min(1.0, weight))  # Обмежуємо значення
            global_vertices.append((v.index, weight))

        # Вихід з режиму редагування
        bpy.ops.object.mode_set(mode='OBJECT')

        # Додаємо вершини до груп
        for v_index, weight in leaves_vertices:
            vg_leaves.add([v_index], weight, 'REPLACE')

        for v_index, weight in global_vertices:
            vg_global.add([v_index], weight, 'REPLACE')
