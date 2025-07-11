import bpy

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

def unregister():
    bpy.utils.unregister_class(PAPL_PT_MainPanel)
    del bpy.types.Scene.papl_light_temperature
    del bpy.types.Scene.pm_sort_method
