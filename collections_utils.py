import bpy 

def create_collection(name, parent=None, color_tag='DEFAULT', disable_in_render=False):
    if not isinstance(name, str):  # Перевіряємо, чи name це рядок
        name = str(name)  # Примусово перетворюємо в рядок

    # Створюємо колекцію
    collection = bpy.data.collections.new(name)
    if parent:
        parent.children.link(collection)
    else:
        bpy.context.scene.collection.children.link(collection)
    
    collection.color_tag = color_tag  # Задаємо колір як атрибут колекції
    
    # Налаштовуємо disable_in_render
    if disable_in_render:
        collection.hide_render = True  # Вимкнути рендер для цієї колекції

    return collection


def create_nested_collections(structure, parent=None):
    for name, value in structure.items():
        if isinstance(value, dict):
            color = value.get("color", "DEFAULT")
            disable_in_render = value.get("disable_in_render", False)
            new_parent = create_collection(
                name,
                parent,
                color,
                disable_in_render
            )
            # Рекурсивно створюємо вкладені колекції
            create_nested_collections({k: v for k, v in value.items() if k != "disable_in_render" and k != "color"}, new_parent)
        else:
            # Якщо значення не є словником, створюємо колекцію
            disable_in_render = False
            create_collection(name, parent, value, disable_in_render)

def create_set_1(main_collection_name):
    collections_structure = {
        main_collection_name: {
            "color": "COLOR_05",
            "###_COMP": {
                "color": "COLOR_07",
                "CC_Cam01": "COLOR_07",
                "CC_Cam02": "COLOR_07",
                "CC_Cam03": "COLOR_07",
                "CC_Cam04": "COLOR_07",
                "CC_Cam05": "COLOR_07"
            },
            "##_Cameras": {"color": "COLOR_06"},
            "#_ASSETS": {
                "color": "COLOR_06",
                "disable_in_render": True,
                "Trees": "COLOR_04",
                "Bushes": "COLOR_04",
                "Grass": "COLOR_04",
                "Props": "COLOR_03",
            },
            "#_HELPERS": {"color": "COLOR_07", "disable_in_render": True},
            "01_BLD": {
                "color": "COLOR_05",
                "Blocking": "COLOR_05",
                "Walls": "COLOR_05",
                "Floor": "COLOR_05",
                "Ceiling": "COLOR_05",
                "Windows": "COLOR_05",
                "Doors": "COLOR_05",
                "Structure": "COLOR_05",
                "Facade": "COLOR_05"
            },
            "02_LANDSCAPE": {
                "color": "COLOR_02",
                "Grass_Plane": "COLOR_02"
            },
            "03_PLANTS": {
                "color": "COLOR_04",
                "Manual": "COLOR_04"
            },
            "04_PROPS": {
                "color": "COLOR_03",
                "Exterior_Props": "COLOR_03",
                "Interior_Props": "COLOR_03",
            },
            "99_HIDE": {
                "color": "COLOR_07", 
                "disable_in_render": True
            }
        },
        "Garbage": {"color": "COLOR_08", "disable_in_render": True}
    }
    create_nested_collections(collections_structure)

def create_set_2(main_collection_name):
    collections_structure = {
        main_collection_name: {
            "color": "COLOR_05",  # Основний колір для проекту
            "###_COMP": {
                "color": "COLOR_07",
                "CC_Cam01": "COLOR_07",
                "CC_Cam02": "COLOR_07",
                "CC_Cam03": "COLOR_07",
                "CC_Cam04": "COLOR_07",
                "CC_Cam05": "COLOR_07"
            },
            "##_Cameras": {"color": "COLOR_06"},
            "№_PLANS": {
                "color": "COLOR_06",
                "Floor_Plan": "COLOR_06",
                "Elevation_Plan": "COLOR_06",
                "Detail_Drawings": "COLOR_06"
            },
            "01_FURNITURE": {
                "color": "COLOR_01",
                "Sofas": "COLOR_01",
                "Tables": "COLOR_01",
                "Chairs": "COLOR_01",
                "Cabinets": "COLOR_01",
                "Shelves": "COLOR_01"
            },
            "02_LIGHTING": {
                "color": "COLOR_02",
                "Ceiling_Lights": "COLOR_02",
                "Floor_Lamps": "COLOR_02",
                "Wall_Lights": "COLOR_02",
                "Table_Lamps": "COLOR_02"
            },
            "03_DECOR": {
                "color": "COLOR_03",
                "Rugs": "COLOR_03",
                "Curtains": "COLOR_03",
                "Wall_Art": "COLOR_03",
                "Decorative_Objects": "COLOR_03"
            },
            "04_STRUCTURE": {
                "color": "COLOR_04",
                "Walls": "COLOR_04",
                "Floors": "COLOR_04",
                "Ceilings": "COLOR_04",
                "Doors": "COLOR_04",
                "Windows": "COLOR_04"
            },
            "07_UTILITIES": {
                "color": "COLOR_05",  # Замінили на допустимий колір
                "Electrical": "COLOR_05",
                "Plumbing": "COLOR_05",
                "HVAC": "COLOR_05"
            },
            "10_HIDE": {
                "color": "COLOR_08",  # Можна використовувати цей колір для прихованих елементів
                "disable_in_render": True
            }
        }
    }
    create_nested_collections(collections_structure)


