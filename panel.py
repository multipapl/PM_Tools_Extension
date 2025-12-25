import bpy

class MaterialProcessorProperties(bpy.types.PropertyGroup):
    texture_folder_path: bpy.props.StringProperty(
        name="Texture Folder",
        description="Path to the folder containing textures",
        subtype='DIR_PATH',
        default="//"
    ) # type: ignore
    transparent_keywords: bpy.props.StringProperty(
        name="Transparent",
        description="Keywords for transparent materials (e.g., leaf, flower)",
        default="leaf"
    ) # type: ignore
    opaque_keywords: bpy.props.StringProperty(
        name="Opaque",
        description="Keywords for opaque materials (e.g., bark, trunk, branch)",
        default="bark, trunk, branch"
    ) # type: ignore

    # Галочки для непрозорих матеріалів
    use_opaque_base_color: bpy.props.BoolProperty(name="Base Color", default=True)
    use_opaque_roughness: bpy.props.BoolProperty(name="Roughness", default=True)
    use_opaque_normal: bpy.props.BoolProperty(name="Normal Map", default=True)
    
    # Галочки для прозорих матеріалів
    use_transparent_base_color: bpy.props.BoolProperty(name="Base Color", default=True)
    use_transparent_opacity: bpy.props.BoolProperty(name="Opacity", default=True)
    use_transparent_normal: bpy.props.BoolProperty(name="Normal Map", default=False)
    use_transparent_translucency: bpy.props.BoolProperty(name="Translucency", default=False)

class PAPL_PT_MainPanel(bpy.types.Panel):
    """Основна панель PM TOOLS"""
    bl_label = "PM TOOLS"
    bl_idname = "PAPL_PT_main_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Papl Tools"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # ========== LAYER MANAGEMENT ==========
        box = layout.box()
        box.label(text="Layer Management", icon='OUTLINER')
        row = box.row()
        row.operator("papl.create_set1", text="Create Set 1", icon='GROUP')
        row.operator("papl.create_set2", text="Create Set 2", icon='GROUP')

        # ========== ORIGIN TOOLS ==========
        box = layout.box()
        box.label(text="Origin Tools", icon='OBJECT_ORIGIN')
        row = box.row()
        row.operator("papl.center_origin", text="Center Origin")
        row.operator("papl.center_bottom_origin", text="Bottom Origin")

        # ========== OPTIMIZATION ==========
        box = layout.box()
        box.label(text="Optimization", icon='MODIFIER')
        row = box.row()
        row.operator("papl.mesh_to_collection_instance", text="Mesh to IC")
        row.operator("papl.adjust_custom_distance", text="DeFuck Lights")
        box.operator("papl.toggle_modifiers", text="Toggle Modifiers", icon='MODIFIER')
        box.operator("papl.cleanup_material_duplicates", text="Delete material duplicate", icon='MATERIAL')

        # ========== UNUSED COLLECTIONS ==========
        box = layout.box()
        box.label(text="Collection Cleanup", icon='COLLECTION_NEW')
        row = box.row()
        row.operator("papl.mark_unused_collections", text="Mark Unused", icon='VIEWZOOM')
        row.operator("papl.delete_unused_collections", text="Delete Unused", icon='TRASH')

        # ========== LIGHTS FROM FACES ==========
        box = layout.box()
        box.label(text="Lights From Faces", icon='LIGHT_SUN')
        box.prop(scene, "lff_visible_to_camera", text="Visible to Camera")
        box.prop(scene, "lff_portal_light", text="Create as Portals")
        box.operator("object.create_lights_from_faces", text="Generate Lights")

        # ========== PROCEDURAL TREE ANIMATION ==========
        box = layout.box()
        box.label(text="Tree Animation", icon='FORCE_WIND')
        row = box.row()
        row.operator("papl.create_vertex_groups", text="Vertex Groups", icon='GROUP_VERTEX')
        row.operator("papl.create_tree_animation", text="Tree Animation", icon='ANIM_DATA')
        box.operator("papl.apply_random_offset", text="Apply Offset", icon='TIME')

        box = layout.box()
        box.label(text="Light Temperature Control", icon='LIGHT')
        # Кнопка для встановлення нодової групи
        box.operator("papl.setup_light_temperature", text="Setup Light Temperature", icon='NODETREE')
        # Переконуємося, що змінна існує перед її відображенням
        if hasattr(context.scene, "papl_light_temperature"):
            box.prop(context.scene, "papl_light_temperature", text="Temperature (K)")
        else:
            box.label(text="⚠️ Property not found!")
        # Кнопка для оновлення температури
        box.operator("papl.update_light_temperature", text="Apply Temperature")

        # ========== Arrange Tools ==========
        box = layout.box()
        box.label(text="Arrange Tools", icon='SORTSIZE')
        box.prop(scene, "pm_sort_method", text="")
        box.operator("papl.arrange_assets", text="Arrange Selected")

        # ========== Material Processor ==========
        box = layout.box()
        box.label(text="Material Processor", icon='MATERIAL')
        
        props = context.scene.material_processor_props
        
        box.prop(props, "texture_folder_path")
        
        # Поля для ключових слів
        split = box.split(factor=0.5)
        col1 = split.column()
        col1.prop(props, "opaque_keywords")
        col2 = split.column()
        col2.prop(props, "transparent_keywords")

        # Дві колонки для налаштувань текстур
        split = box.split(factor=0.5)
        
        # Ліва колонка для непрозорих
        col1 = split.column()
        sub_box1 = col1.box()
        sub_box1.label(text="Opaque Textures:")
        sub_box1.prop(props, "use_opaque_base_color")
        sub_box1.prop(props, "use_opaque_roughness")
        sub_box1.prop(props, "use_opaque_normal")

        # Права колонка для прозорих
        col2 = split.column()
        sub_box2 = col2.box()
        sub_box2.label(text="Transparent Textures:")
        sub_box2.prop(props, "use_transparent_base_color")
        sub_box2.prop(props, "use_transparent_opacity")
        sub_box2.prop(props, "use_transparent_normal")
        sub_box2.prop(props, "use_transparent_translucency")
        
        box.operator("asset.process_materials", text="Process Materials", icon='TRIA_RIGHT_BAR')

        # ========== CAMERA TOOLS ==========
        box = layout.box()
        box.label(text="Camera Tools", icon='CAMERA_DATA')
        row = box.row()
        row.operator("papl.convert_max_cameras", text="Max Empties to Cams", icon='FORWARD')


def register():
    bpy.utils.register_class(PAPL_PT_MainPanel)
    bpy.types.Scene.papl_light_temperature = bpy.props.FloatProperty(
        name="Light Temperature",
        description="Set temperature for selected lights",
        default=3500,
        min=1000,
        max=10000
    )
    bpy.types.Scene.pm_sort_method = bpy.props.EnumProperty(
        name="Sort By",
        description="Метод сортування об'єктів перед розстановкою",
        items=[
            ('POLYCOUNT', "By Polycount", "Сортувати за кількістю полігонів"),
            ('SIZE', "By Size", "Сортувати за об'ємом (по габаритах)"),
        ],
        default='POLYCOUNT'
    )
        # Реєструємо властивості для матеріального процесора
    bpy.utils.register_class(MaterialProcessorProperties)
    bpy.types.Scene.material_processor_props = bpy.props.PointerProperty(type=MaterialProcessorProperties)

def unregister():
    bpy.utils.unregister_class(PAPL_PT_MainPanel)
    del bpy.types.Scene.papl_light_temperature
    del bpy.types.Scene.pm_sort_method
    # Видаляємо властивості матеріального процесора
    bpy.utils.unregister_class(MaterialProcessorProperties)
    del bpy.types.Scene.material_processor_props
