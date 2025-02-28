import bpy

def mark_unused_collections(library_scene_name="Library", marker="[UNUSED] "):
    """Позначає колекції у сцені 'Library', які не інстанційовані в інших сценах."""
    
    if library_scene_name not in bpy.data.scenes:
        return None, None, "❌ Сцена не знайдена!"

    library_scene = bpy.data.scenes[library_scene_name]
    library_collections = set(library_scene.collection.children)  # Отримуємо всі колекції у Library

    instantiated_collections = set()
    for scene in bpy.data.scenes:
        if scene.name == library_scene_name:
            continue  # Пропускаємо саму сцену Library
        for obj in scene.objects:
            if obj.instance_type == 'COLLECTION' and obj.instance_collection:
                instantiated_collections.add(obj.instance_collection)

    marked_count = 0
    cleaned_count = 0

    for collection in library_collections:
        if collection not in instantiated_collections:
            if not collection.name.startswith(marker):
                collection.name = marker + collection.name
                marked_count += 1
        else:
            if collection.name.startswith(marker):
                collection.name = collection.name[len(marker):]
                cleaned_count += 1

    return marked_count, cleaned_count, None
