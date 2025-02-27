import bpy
from .collections_utils import create_set_1, create_set_2
from .origin_utils import center_origin, center_bottom_origin
from .optimization import replace_meshes_with_instance
from .light_utils import create_lights_from_faces
from .light_unfuck import adjust_custom_distance
from .vertex_groups import create_tree_vertex_groups
from .tree_animation import create_tree_animation
from .random_offset import apply_random_offset

""" from papl_tools.collections_utils import create_set_1, create_set_2
from papl_tools.origin_utils import center_origin, center_bottom_origin  
from papl_tools.optimization import replace_meshes_with_instance
from papl_tools.light_utils import create_lights_from_faces
from papl_tools.light_unfuck import adjust_custom_distance
from papl_tools.vertex_groups import create_tree_vertex_groups
from papl_tools.tree_animation import create_tree_animation
from papl_tools.random_offset import apply_random_offset """

# Оператор для створення набору 1
class PAPL_OT_CreateSet1(bpy.types.Operator):
    bl_idname = "papl.create_set1"
    bl_label = "Create Collection Set 1"
    
    main_collection_name: str = bpy.props.StringProperty(
        name="Main Collection Name",
        default="ProjectName"
    )

    def execute(self, context):
        create_set_1(self.main_collection_name)
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

# Оператор для створення набору 2
class PAPL_OT_CreateSet2(bpy.types.Operator):
    bl_idname = "papl.create_set2"
    bl_label = "Create Collection Set 2"

    main_collection_name: str = bpy.props.StringProperty(
        name="Main Collection Name",
        default="ProjectName"
    )

    def execute(self, context):
        create_set_2(self.main_collection_name)
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

# Оператор для центрування оріджину
class PAPL_OT_CenterOrigin(bpy.types.Operator):
    bl_idname = "papl.center_origin"
    bl_label = "Center Origin"
    
    def execute(self, context):
        center_origin()  # Викликаємо функцію для центрування оріджину
        return {'FINISHED'}

# Оператор для центрування оріджину з позицією на дні
class PAPL_OT_CenterBottomOrigin(bpy.types.Operator):
    bl_idname = "papl.center_bottom_origin"
    bl_label = "Center + Bottom Origin"
    
    def execute(self, context):
        center_bottom_origin()  
        return {'FINISHED'}
        
# Оператор для конвертування мешів на інстанс колекції
class PAPL_OT_MeshToCollectionInstance(bpy.types.Operator):
    bl_idname = "papl.mesh_to_collection_instance"
    bl_label = "Meshes to Collection Instances"
    
    def execute(self, context):
        replace_meshes_with_instance()  
        return {'FINISHED'}
        
class OT_CreateLightsFromFaces(bpy.types.Operator):
    bl_idname = "object.create_lights_from_faces"
    bl_label = "Create Lights from Faces"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (
            context.active_object is not None and 
            context.active_object.type == 'MESH' and 
            context.mode == 'EDIT_MESH'
        )

    def execute(self, context):
        scene = context.scene
        obj = context.active_object
        result = create_lights_from_faces(
            obj,
            scene.lff_portal_light,
            scene.lff_visible_to_camera
        )

        if result == "No faces selected":
            self.report({'WARNING'}, result)
            return {'CANCELLED'}

        self.report({'INFO'}, result)
        return {'FINISHED'}
        
class LIGHTS_OT_AdjustCustomDistance(bpy.types.Operator):
    """Зменшує Custom Distance у вибраних світильників у 100 разів"""
    bl_idname = "papl.adjust_custom_distance"
    bl_label = "Lights UnFuck"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        adjust_custom_distance()
        return {'FINISHED'}

class PAPL_OT_ApplyRandomOffset(bpy.types.Operator):
    """Застосовує випадковий Offset для Noise-модифікаторів"""
    bl_idname = "papl.apply_random_offset"
    bl_label = "Apply Random Offset"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        apply_random_offset()
        return {'FINISHED'}

class PAPL_OT_CreateVertexGroups(bpy.types.Operator):
    """Створює вертекс-групи для анімації дерев"""
    bl_idname = "papl.create_vertex_groups"
    bl_label = "Create Vertex Groups"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        create_tree_vertex_groups()
        return {'FINISHED'}
  
class PAPL_OT_CreateTreeAnimation(bpy.types.Operator):
    """Створює анімацію для дерев"""
    bl_idname = "papl.create_tree_animation"
    bl_label = "Create Tree Animation"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        create_tree_animation()
        return {'FINISHED'}
        

def register():
    bpy.utils.register_class(PAPL_OT_CreateSet1)
    bpy.utils.register_class(PAPL_OT_CreateSet2)
    bpy.utils.register_class(PAPL_OT_CenterOrigin)
    bpy.utils.register_class(PAPL_OT_CenterBottomOrigin)
    bpy.utils.register_class(PAPL_OT_MeshToCollectionInstance)
    bpy.utils.register_class(OT_CreateLightsFromFaces)
    bpy.utils.register_class(LIGHTS_OT_AdjustCustomDistance)
    bpy.utils.register_class(PAPL_OT_CreateVertexGroups)
    bpy.utils.register_class(PAPL_OT_CreateTreeAnimation)
    bpy.utils.register_class(PAPL_OT_ApplyRandomOffset)

def unregister():
    bpy.utils.unregister_class(PAPL_OT_CreateSet1)
    bpy.utils.unregister_class(PAPL_OT_CreateSet2)
    bpy.utils.unregister_class(PAPL_OT_CenterOrigin)
    bpy.utils.unregister_class(PAPL_OT_CenterBottomOrigin)
    bpy.utils.unregister_class(PAPL_OT_MeshToCollectionInstance)
    bpy.utils.unregister_class(OT_CreateLightsFromFaces)
    bpy.utils.unregister_class(LIGHTS_OT_AdjustCustomDistance)
    bpy.utils.unregister_class(PAPL_OT_CreateVertexGroups)
    bpy.utils.unregister_class(PAPL_OT_CreateTreeAnimation)
    bpy.utils.unregister_class(PAPL_OT_ApplyRandomOffset)
