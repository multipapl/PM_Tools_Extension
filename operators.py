import bpy
from .collections_utils import create_set_1, create_set_2
from .origin_utils import center_origin, center_bottom_origin
from .optimization import replace_meshes_with_instance
from .light_utils import create_lights_from_faces
from .light_unfuck import adjust_custom_distance
from .vertex_groups import create_tree_vertex_groups
from .tree_animation import create_tree_animation
from .random_offset import apply_random_offset
from .toggle_modifiers import toggle_modifiers_by_name
from .toggle_unused_collections import mark_unused_collections, delete_unused_collections
from .toggle_light_temperature import update_light_temperature
from .toggle_light_temperature import setup_light_temperature_for_selected_lights
from .materials_tools import cleanup_duplicates_in_selected_objects
from .arrange_utils import arrange_objects_logic
from .maxtree_converter import process_materials
from .camera_utils import convert_max_empties_to_cameras

# Оператор для створення набору 1
class PAPL_OT_CreateSet1(bpy.types.Operator):
    bl_idname = "papl.create_set1"
    bl_label = "Create Collection Set 1"

    # Коректне визначення властивості
    __annotations__ = {
        "main_collection_name": bpy.props.StringProperty(
            name="Main Collection Name",
            default="ProjectName"
        )
    }

    def execute(self, context):
        print(f"Creating collection: {self.main_collection_name}")  # Дебаг-лог
        create_set_1(self.main_collection_name)
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


# Оператор для створення набору 2
class PAPL_OT_CreateSet2(bpy.types.Operator):
    bl_idname = "papl.create_set2"
    bl_label = "Create Collection Set 2"

    __annotations__ = {
        "main_collection_name": bpy.props.StringProperty(
            name="Main Collection Name",
            default="ProjectName"
        )
    }

    def execute(self, context):
        print(f"Creating collection: {self.main_collection_name}")  # Дебаг-лог
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
    
class PAPL_OT_ToggleModifiers(bpy.types.Operator):
    """Перемикає видимість модифікаторів за назвою"""
    bl_idname = "papl.toggle_modifiers"
    bl_label = "Toggle Modifiers"
    bl_options = {'REGISTER', 'UNDO'}
    
    # Виносимо властивість у клас
    __annotations__ = {
        "modifier_name": bpy.props.StringProperty(
            name="Modifier Name",
            description="Enter the name of the modifier to toggle",
            default="Proxy"
        )
    }

    def execute(self, context):
        toggle_modifiers_by_name(self.modifier_name)
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
class PAPL_OT_MarkUnusedCollections(bpy.types.Operator):
    """Позначає невикористані колекції у сцені Library"""
    bl_idname = "papl.mark_unused_collections"
    bl_label = "Mark Unused Collections"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        marked, cleaned, error = mark_unused_collections()
        
        if error:
            self.report({'ERROR'}, error)
        elif marked > 0:
            self.report({'INFO'}, f"⚠ Позначено {marked} невикористаних колекцій!")
        else:
            self.report({'INFO'}, "✅ Усі колекції використовуються. Сцена чиста!")

        if cleaned > 0:
            self.report({'INFO'}, f"🔄 Відновлено {cleaned} колекцій!")

        return {'FINISHED'}
    
class PAPL_OT_DeleteUnusedCollections(bpy.types.Operator):
    """Видаляє всі позначені як `[UNUSED]` колекції у сцені 'Library'"""
    bl_idname = "papl.delete_unused_collections"
    bl_label = "Delete Unused Collections"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        error, deleted_count = delete_unused_collections()
        
        if error:
            self.report({'ERROR'}, error)
        elif deleted_count > 0:
            self.report({'INFO'}, f"🗑 Видалено {deleted_count} невикористаних колекцій!")
        else:
            self.report({'INFO'}, "✅ Немає невикористаних колекцій для видалення.")

        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)
    
class PAPL_OT_UpdateLightTemperature(bpy.types.Operator):
    """Updates the temperature in the PAPL_LightTemperature node for selected lights."""
    bl_idname = "papl.update_light_temperature"
    bl_label = "Update Light Temperature"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Отримуємо значення температури з сцени як float
        new_temperature = context.scene.papl_light_temperature

        if isinstance(new_temperature, (int, float)):
            update_light_temperature(float(new_temperature))
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "Invalid temperature value! Must be a number.")
            return {'CANCELLED'}

class PAPL_OT_SetupLightTemperature(bpy.types.Operator):
    """Sets up the PAPL_LightTemperature node group for selected lights."""
    bl_idname = "papl.setup_light_temperature"
    bl_label = "Setup Light Temperature"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        try:
            setup_light_temperature_for_selected_lights()
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to setup light temperature: {e}")
            return {'CANCELLED'}
        return {'FINISHED'}
    
class PAPL_OT_CleanupMaterialDuplicates(bpy.types.Operator):
    bl_idname = "papl.cleanup_material_duplicates"
    bl_label = "Очистити дублікати матеріалів"
    bl_description = "Замінює дублікати матеріалів у вибраних обʼєктах на оригінальні"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        count = cleanup_duplicates_in_selected_objects()
        if count == 0:
            self.report({'INFO'}, "Нічого не знайдено для заміни.")
            return {'CANCELLED'}
        self.report({'INFO'}, f"✅ Заміна завершена: {count} матеріал(ів) оновлено.")
        return {'FINISHED'}

class PAPI_OT_ArrangeAssets(bpy.types.Operator):
    """Розставляє виділені об'єкти в ряд"""
    bl_idname = "papl.arrange_assets"
    bl_label = "Arrange Assets"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        sort_method = context.scene.pm_sort_method
        success, message = arrange_objects_logic(context.selected_objects, sort_method)
        if success:
            self.report({'INFO'}, message)
        else:
            self.report({'WARNING'}, message)
        return {'FINISHED'}
    
class ASSET_OT_ProcessMaterials(bpy.types.Operator):
    """Finds and connects textures for materials of selected objects"""
    bl_idname = "asset.process_materials"
    bl_label = "Process Materials"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.material_processor_props
        selected_objects = context.selected_objects
        if not selected_objects:
            self.report({'WARNING'}, "No objects selected")
            return {'CANCELLED'}
        materials_to_process = set()
        for obj in selected_objects:
            if obj.type == 'MESH':
                for mat_slot in obj.material_slots:
                    if mat_slot.material:
                        materials_to_process.add(mat_slot.material)
        if not materials_to_process:
            self.report({'WARNING'}, "Selected objects have no materials")
            return {'CANCELLED'}
            
        opaque_maps_to_use = {
            'BASE_COLOR': props.use_opaque_base_color,
            'ROUGHNESS': props.use_opaque_roughness,
            'NORMAL': props.use_opaque_normal,
        }
        transparent_maps_to_use = {
            'BASE_COLOR': props.use_transparent_base_color,
            'ALPHA': props.use_transparent_opacity,
            'NORMAL': props.use_transparent_normal,
            'TRANSLUCENCY': props.use_transparent_translucency,
        }

        processed, errors = process_materials(
            context, list(materials_to_process), opaque_maps_to_use, transparent_maps_to_use
        )

        if errors > 0:
             self.report({'ERROR'}, f"Finished with {errors} errors. Check console.")
        else:
             self.report({'INFO'}, f"Successfully processed {processed} materials.")
        
        # --- ДОДАНО: Очищення даних анімації ---
        animation_cleared_count = 0
        for obj in selected_objects:
            if obj.animation_data:
                obj.animation_data_clear()
                animation_cleared_count += 1
        
        if animation_cleared_count > 0:
            self.report({'INFO'}, f"Animation data cleared from {animation_cleared_count} objects.")

        return {'FINISHED'}

class PAPL_OT_ConvertMaxCameras(bpy.types.Operator):
    """Конвертує пари Empty + Empty.Target з 3ds Max у камери Blender"""
    bl_idname = "papl.convert_max_cameras"
    bl_label = "Convert Max Cameras"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        count = convert_max_empties_to_cameras()
        if count > 0:
            self.report({'INFO'}, f"Успішно створено {count} камер")
        else:
            self.report({'WARNING'}, "Не знайдено підходящих пар Empty + Target")
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
    bpy.utils.register_class(PAPL_OT_ToggleModifiers)
    bpy.utils.register_class(PAPL_OT_MarkUnusedCollections)
    bpy.utils.register_class(PAPL_OT_DeleteUnusedCollections)
    bpy.utils.register_class(PAPL_OT_UpdateLightTemperature)
    bpy.utils.register_class(PAPL_OT_SetupLightTemperature)
    bpy.utils.register_class(PAPL_OT_CleanupMaterialDuplicates)
    bpy.utils.register_class(PAPI_OT_ArrangeAssets)
    bpy.utils.register_class(ASSET_OT_ProcessMaterials)
    bpy.utils.register_class(PAPL_OT_ConvertMaxCameras)


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
    bpy.utils.unregister_class(PAPL_OT_ToggleModifiers)
    bpy.utils.unregister_class(PAPL_OT_MarkUnusedCollections)
    bpy.utils.unregister_class(PAPL_OT_DeleteUnusedCollections)
    bpy.utils.unregister_class(PAPL_OT_UpdateLightTemperature)
    bpy.utils.unregister_class(PAPL_OT_SetupLightTemperature)
    bpy.utils.unregister_class(PAPL_OT_CleanupMaterialDuplicates)
    bpy.utils.unregister_class(PAPI_OT_ArrangeAssets)
    bpy.utils.unregister_class(ASSET_OT_ProcessMaterials)
    bpy.utils.unregister_class(PAPL_OT_ConvertMaxCameras)
