# /your_addon/maxtree_converter.py

import bpy
import os
import re

# --- КОНФІГУРАЦІЯ ---
LEAF_SHADER_INFO = {
    'node_group_name': 'PAPL_LeafShader',
    'socket_map': {
        'BASE_COLOR': 'Base Color', 'ALPHA': 'Opacity',
        'NORMAL': 'Normal', 'TRANSLUCENCY': 'Translusency',
    }
}
TEXTURE_SUFFIXES = {
    'BASE_COLOR': ['_d', '_diff', '_albedo', '_col'],
    'ALPHA': ['_a', '_alpha', '_mask', '_opacity'],
    'ROUGHNESS': ['_r', '_rough', '_roughness'],
    'NORMAL': ['_n', '_nrm', '_normal'],
    'TRANSLUCENCY': ['_trans', '_sss', '_transl', '_translucency'],
    'GLOSS': ['_g', '_gloss', '_glossiness']
}

# --- ДОПОМІЖНІ ФУНКЦІЇ ---

def find_asset_id(material_name, keywords):
    """
    Знаходить ID ассету. Спочатку шукає "слово_число", якщо не знаходить - повертає просто "слово".
    """
    mat_name_lower = material_name.lower().replace(" ", "_")
    for keyword in keywords:
        if keyword in mat_name_lower:
            match_with_digit = re.search(f"({keyword}[_]*\\d+)", mat_name_lower)
            if match_with_digit:
                return match_with_digit.group(1)
            return keyword
    return None

def find_texture_path(asset_id, tex_type, texture_folder, texture_files):
    """
    Знаходить шлях до текстури, шукаючи asset_id та суфікс у назві файлу.
    """
    suffixes = TEXTURE_SUFFIXES.get(tex_type, [])
    for filename in texture_files:
        fn_lower = filename.lower().replace(" ", "_")
        if asset_id in fn_lower:
            for suffix in suffixes:
                # ВИПРАВЛЕНО: Пошук став точнішим, щоб уникнути часткових збігів (напр. "_d" в "_directx")
                # Тепер він шукає суфікс, після якого йде або крапка, або інше підкреслення.
                pattern = f"{re.escape(suffix)}(\\.|_)"
                if re.search(pattern, fn_lower):
                    return os.path.join(texture_folder, filename)
    return None

def create_texture_node(nodes, path, tex_type, y_pos):
    """Створює ноду текстури і відразу встановлює правильний колірний простір."""
    tex_node = nodes.new('ShaderNodeTexImage')
    tex_node.image = bpy.data.images.load(path, check_existing=True)
    tex_node.location = (-650, y_pos)
    if tex_type == 'BASE_COLOR':
        tex_node.image.colorspace_settings.name = 'sRGB'
    else:
        tex_node.image.colorspace_settings.name = 'Non-Color'
    return tex_node

# --- ГОЛОВНА ФУНКЦІЯ ---
def process_materials(context, materials_to_process, opaque_maps_to_use, transparent_maps_to_use):
    props = context.scene.material_processor_props
    texture_folder = bpy.path.abspath(props.texture_folder_path)
    if not os.path.isdir(texture_folder): return 0, 1

    transparent_keywords = [k.strip().lower() for k in props.transparent_keywords.split(',') if k.strip()]
    opaque_keywords = [k.strip().lower() for k in props.opaque_keywords.split(',') if k.strip()]
    all_keywords = transparent_keywords + opaque_keywords
    
    try:
        texture_files = os.listdir(texture_folder)
    except FileNotFoundError: return 0, 1

    processed_count = 0
    for mat in materials_to_process:
        if not mat or not mat.use_nodes: continue
        
        asset_id = find_asset_id(mat.name, all_keywords)
        if not asset_id: continue

        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        for node in nodes:
            if node.type != 'OUTPUT_MATERIAL': nodes.remove(node)
        output_node = nodes.get('Material Output') or nodes.new('ShaderNodeOutputMaterial')
        
        y_pos = 0
        y_offset = -350
        
        # --- ОБРОБКА ПРОЗОРИХ МАТЕРІАЛІВ ---
        if any(keyword in asset_id for keyword in transparent_keywords):
            try:
                shader = nodes.new('ShaderNodeGroup')
                shader.node_tree = bpy.data.node_groups[LEAF_SHADER_INFO['node_group_name']]
                shader.location = (-250, 0)
                links.new(shader.outputs[0], output_node.inputs['Surface'])
                socket_map = LEAF_SHADER_INFO['socket_map']
                
                base_color_node = None
                if transparent_maps_to_use.get('BASE_COLOR'):
                    path = find_texture_path(asset_id, 'BASE_COLOR', texture_folder, texture_files)
                    if path:
                        base_color_node = create_texture_node(nodes, path, 'BASE_COLOR', y_pos)
                        links.new(base_color_node.outputs['Color'], shader.inputs[socket_map['BASE_COLOR']])
                        y_pos += y_offset
                if transparent_maps_to_use.get('ALPHA'):
                    path = find_texture_path(asset_id, 'ALPHA', texture_folder, texture_files)
                    if path:
                        tex_node = create_texture_node(nodes, path, 'ALPHA', y_pos)
                        links.new(tex_node.outputs['Color'], shader.inputs[socket_map['ALPHA']])
                        y_pos += y_offset
                    elif base_color_node:
                        links.new(base_color_node.outputs['Alpha'], shader.inputs[socket_map['ALPHA']])
                if transparent_maps_to_use.get('NORMAL'):
                    path = find_texture_path(asset_id, 'NORMAL', texture_folder, texture_files)
                    if path:
                        tex_node = create_texture_node(nodes, path, 'NORMAL', y_pos)
                        links.new(tex_node.outputs['Color'], shader.inputs[socket_map['NORMAL']])
                        y_pos += y_offset
                if transparent_maps_to_use.get('TRANSLUCENCY'):
                    path = find_texture_path(asset_id, 'TRANSLUCENCY', texture_folder, texture_files)
                    if path:
                        tex_node = create_texture_node(nodes, path, 'TRANSLUCENCY', y_pos)
                        links.new(tex_node.outputs['Color'], shader.inputs[socket_map['TRANSLUCENCY']])
                        y_pos += y_offset

            except KeyError: continue

        # --- ОБРОБКА НЕПРОЗОРИХ МАТЕРІАЛІВ ---
        elif any(keyword in asset_id for keyword in opaque_keywords):
            shader = nodes.new('ShaderNodeBsdfPrincipled')
            shader.location = (-250, 0)
            links.new(shader.outputs[0], output_node.inputs['Surface'])
            
            if opaque_maps_to_use.get('BASE_COLOR'):
                path = find_texture_path(asset_id, 'BASE_COLOR', texture_folder, texture_files)
                if path:
                    tex_node = create_texture_node(nodes, path, 'BASE_COLOR', y_pos)
                    links.new(tex_node.outputs['Color'], shader.inputs['Base Color'])
                    y_pos += y_offset
            if opaque_maps_to_use.get('NORMAL'):
                path = find_texture_path(asset_id, 'NORMAL', texture_folder, texture_files)
                if path:
                    tex_node = create_texture_node(nodes, path, 'NORMAL', y_pos)
                    normal_map_node = nodes.new('ShaderNodeNormalMap')
                    normal_map_node.location = (-400, y_pos)
                    links.new(tex_node.outputs['Color'], normal_map_node.inputs['Color'])
                    links.new(normal_map_node.outputs['Normal'], shader.inputs['Normal'])
                    y_pos += y_offset
            if opaque_maps_to_use.get('ROUGHNESS'):
                rough_path = find_texture_path(asset_id, 'ROUGHNESS', texture_folder, texture_files)
                if rough_path:
                    tex_node = create_texture_node(nodes, rough_path, 'ROUGHNESS', y_pos)
                    links.new(tex_node.outputs['Color'], shader.inputs['Roughness'])
                else:
                    gloss_path = find_texture_path(asset_id, 'GLOSS', texture_folder, texture_files)
                    if gloss_path:
                        tex_node = create_texture_node(nodes, gloss_path, 'GLOSS', y_pos)
                        invert_node = nodes.new('ShaderNodeInvert')
                        invert_node.location = (-400, y_pos)
                        links.new(tex_node.outputs['Color'], invert_node.inputs['Color'])
                        links.new(invert_node.outputs['Color'], shader.inputs['Roughness'])

        processed_count += 1
        
    return processed_count, 0