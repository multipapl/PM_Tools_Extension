import bpy

def ensure_light_temperature_node_group():
    """Creates the 'PAPL_LightTemperature' node group if it does not exist."""
    
    node_group_name = "PAPL_LightTemperature"

    # Перевіряємо, чи вже існує нодова група
    if node_group_name in bpy.data.node_groups:
        return bpy.data.node_groups[node_group_name]

    # Створюємо нову нодову групу
    light_temp_group = bpy.data.node_groups.new(name=node_group_name, type='ShaderNodeTree')

    # Додаємо Input та Output
    input_node = light_temp_group.nodes.new(type="NodeGroupInput")
    input_node.location = (-300, 0)

    output_node = light_temp_group.nodes.new(type="NodeGroupOutput")
    output_node.location = (300, 0)

    # Створюємо Blackbody ноду
    blackbody_node = light_temp_group.nodes.new(type="ShaderNodeBlackbody")
    blackbody_node.location = (0, 0)
    blackbody_node.inputs[0].default_value = 3500  # За замовчуванням 3500K

    # Додаємо інпут "Temperature"
    light_temp_group.inputs.new("NodeSocketFloat", "Temperature")
    light_temp_group.inputs["Temperature"].default_value = 3500  # Значення за замовчуванням

    # Додаємо аутпут "Color"
    light_temp_group.outputs.new("NodeSocketColor", "Color")

    # З'єднуємо вузли
    light_temp_group.links.new(input_node.outputs["Temperature"], blackbody_node.inputs[0])
    light_temp_group.links.new(blackbody_node.outputs[0], output_node.inputs["Color"])

    print(f"✅ Node group '{node_group_name}' created successfully!")
    return light_temp_group

def setup_light_temperature_for_selected_lights():
    """Sets up the 'PAPL_LightTemperature' node group for selected lights in the scene."""
    
    node_group = ensure_light_temperature_node_group()  # Переконуємося, що нода існує
    node_group_name = node_group.name  # Отримуємо назву нодової групи

    # Перебираємо всі вибрані об'єкти
    for obj in bpy.context.selected_objects:
        if obj.type == 'LIGHT':  # Переконуємося, що це світильник
            light = obj.data

            # Активуємо Use Nodes, якщо не активовано
            if not light.use_nodes:
                light.use_nodes = True

            # Отримуємо нодовий матеріал світильника
            nodes = light.node_tree.nodes
            links = light.node_tree.links

            # Перевіряємо, чи вже є PAPL_LightTemperature нода
            temp_node = None
            for node in nodes:
                if node.type == 'GROUP' and node.node_tree and node.node_tree.name == node_group_name:
                    temp_node = node
                    break

            # Якщо такої ноди ще немає - створюємо
            if not temp_node:
                temp_node = nodes.new(type='ShaderNodeGroup')
                temp_node.node_tree = bpy.data.node_groups[node_group_name]
                temp_node.location = (-200, 0)  # Розміщуємо поруч

            # Отримуємо Emission Shader
            emission_node = None
            for node in nodes:
                if node.type == 'EMISSION':
                    emission_node = node
                    break

            # Якщо немає Emission, знаходимо вихід Material Output
            if not emission_node:
                for node in nodes:
                    if node.type == 'OUTPUT_LIGHT':
                        emission_node = node.inputs["Surface"].links[0].from_node
                        break
            
            # Якщо знайдено Emission, підключаємо нодову групу до Color
            if emission_node:
                links.new(temp_node.outputs[0], emission_node.inputs["Color"])

            print(f"✅ '{node_group_name}' node group added for {obj.name}")

def update_light_temperature(new_temperature):
    """Updates the temperature value in the 'PAPL_LightTemperature' node for selected lights."""
    
    node_group_name = "PAPL_LightTemperature"

    # Перевіряємо, чи існує нодова група
    if node_group_name not in bpy.data.node_groups:
        print(f"❌ Node group '{node_group_name}' not found!")
        return

    # Переконуємося, що значення є float
    try:
        new_temperature = float(new_temperature)  # Примусове перетворення у float
    except ValueError:
        print("❌ Invalid temperature value! It must be a number.")
        return

    # Перебираємо всі вибрані об'єкти
    for obj in bpy.context.selected_objects:
        if obj.type == 'LIGHT':  # Переконуємося, що це світильник
            light = obj.data

            # Якщо Use Nodes не увімкнено – пропускаємо цей світильник
            if not light.use_nodes:
                continue

            nodes = light.node_tree.nodes

            # Шукаємо ноду групи PAPL_LightTemperature
            for node in nodes:
                if node.type == 'GROUP' and node.node_tree and node.node_tree.name == node_group_name:
                    # Перевіряємо, чи існує вхід 'Temperature'
                    if "Temperature" in node.inputs:
                        node.inputs["Temperature"].default_value = new_temperature
                        print(f"✅ Temperature set to {new_temperature}K for {obj.name}")
                    else:
                        print(f"⚠️ '{node_group_name}' in {obj.name} does not have a 'Temperature' input!")
                    break

