import bpy

class PAPL_PT_MainPanel(bpy.types.Panel):
    bl_label = "PM Tools"
    bl_idname = "PAPL_PT_main_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Papl Tools"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # Створюємо підкатегорію для наборів шарів
        box = layout.box()
        box.label(text="Create Layer Sets")
        box.operator("papl.create_set1")
        box.operator("papl.create_set2")
        
        # Створюємо підкатегорію для Origin Placer
        box = layout.box()
        box.label(text="Origin Placer")
        box.operator("papl.center_origin")
        box.operator("papl.center_bottom_origin")
        
        # Створюємо підкатегорію для Optimization
        box = layout.box()
        box.label(text="Optimize")
        box.operator("papl.mesh_to_collection_instance")
        box.operator("papl.adjust_custom_distance")
        
        # Створюємо підкатегорію для Lights From Faces
        box = layout.box()
        box.label(text="Lights From Faces")
        box.prop(scene, "lff_visible_to_camera", text="Visible to Camera")
        box.prop(scene, "lff_portal_light", text="Create as Portals")
        box.operator("object.create_lights_from_faces")
        
        # Новий бокс для кнопки створення вертекс-груп
        box = layout.box()
        box.label(text="Procedural Tree Animation")
        box.operator("papl.create_vertex_groups", text="Create Vertex Groups")
        box.operator("papl.create_tree_animation", text="Create Tree Animation")
        box.operator("papl.apply_random_offset", text="Apply Random Offset")
              

def register():
    bpy.utils.register_class(PAPL_PT_MainPanel)

def unregister():
    bpy.utils.unregister_class(PAPL_PT_MainPanel)
