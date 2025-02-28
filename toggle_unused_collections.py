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
        # Якщо назва починається з "GS", ми її не чіпаємо
        if collection.name.startswith("GS"):
            continue

        if collection not in instantiated_collections:
            if not collection.name.startswith(marker):
                collection.name = marker + collection.name
                marked_count += 1
        else:
            if collection.name.startswith(marker):
                collection.name = collection.name[len(marker):]
                cleaned_count += 1

    return marked_count, cleaned_count, None

def delete_unused_collections(library_scene_name="Library", marker="[UNUSED] "):
    """Видаляє всі колекції, які позначені як `[UNUSED]` у сцені 'Library'."""
    
    if library_scene_name not in bpy.data.scenes:
        return "❌ Сцена не знайдена!", 0

    library_scene = bpy.data.scenes[library_scene_name]
    collections_to_delete = [col for col in library_scene.collection.children if col.name.startswith(marker)]

    deleted_count = 0
    for collection in collections_to_delete:
        bpy.data.collections.remove(collection)
        deleted_count += 1

    return None, deleted_count