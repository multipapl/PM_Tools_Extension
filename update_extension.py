""" # 🔹 Налаштування шляхів
EXTENSION_NAME = "papl_tools"  # Назва розширення
VERSION_FILE = "version.txt"   # Файл для збереження останньої версії
REPO_DIR = Path("C:/Blender_Extensions_Repo/packages")  # Шлях до папки репозиторію
EXTENSION_DIR = Path("Q:/_LIB/Blender/Papl_Tools")  # ЗАМІНИ на свій шлях
INDEX_FILE = REPO_DIR / "index.json"  # Файл index.json """

import os
import json
import hashlib
import zipfile

# === Налаштування ===
EXTENSION_NAME = "papl_tools"
REPO_DIR = r"C:/Blender_Extensions_Repo/packages"  # Де лежить index.json та архіви
VERSION_FILE = os.path.join(REPO_DIR, "version.txt")  # Файл для збереження версії
INDEX_FILE = os.path.join(REPO_DIR, "index.json")  # Файл index.json
EXTENSION_DIR = r"Q:/_LIB/Blender/Papl_Tools"  # Шлях до коду розширення
INIT_FILE = os.path.join(EXTENSION_DIR, "__init__.py")  # Головний файл аддона

# === Отримання поточної версії ===
def get_current_version():
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, "r") as f:
            return f.read().strip()
    return "1.0.0"

# === Оновлення версії ===
def increment_version(version):
    major, minor, patch = map(int, version.split("."))
    patch += 1
    return f"{major}.{minor}.{patch}"

current_version = get_current_version()
new_version = increment_version(current_version)

# === Оновлюємо версію у version.txt ===
with open(VERSION_FILE, "w") as f:
    f.write(new_version)

# === Оновлення версії у __init__.py (щоб ZIP містив актуальну версію) ===
if os.path.exists(INIT_FILE):
    with open(INIT_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    with open(INIT_FILE, "w", encoding="utf-8") as f:
        for line in lines:
            if line.startswith("bl_info"):
                f.write(f'bl_info = {{"version": "{new_version}"}}\n')
            else:
                f.write(line)

# === Створення ZIP-архіву ===
zip_filename = f"{EXTENSION_NAME}-{new_version}.zip"
zip_path = os.path.join(REPO_DIR, zip_filename)

with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
    for root, _, files in os.walk(EXTENSION_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, EXTENSION_DIR)
            zipf.write(file_path, arcname)

# === Генерація SHA256-хешу ===
def calculate_hash(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return f"sha256:{sha256.hexdigest()}"

archive_hash = calculate_hash(zip_path)
archive_size = os.path.getsize(zip_path)

# === Оновлення index.json ===
if os.path.exists(INDEX_FILE):
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        index_data = json.load(f)
    
    # Оновлюємо необхідні поля
    index_data["data"][0]["version"] = new_version
    index_data["data"][0]["schema_version"] = new_version  # Оновлення schema_version
    index_data["data"][0]["archive_url"] = f"./{zip_filename}"
    index_data["data"][0]["archive_size"] = archive_size
    index_data["data"][0]["archive_hash"] = archive_hash

    # Записуємо оновлений index.json
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index_data, f, indent=4, ensure_ascii=False)

    print(f"✅ Оновлено {INDEX_FILE} для версії {new_version}")

print(f"📦 Архів збережено: {zip_path}")
print(f"📜 Index.json оновлено: {INDEX_FILE}")

