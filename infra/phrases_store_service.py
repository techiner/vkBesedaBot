import os
import json

PHRASES_FILEPATH = './data/phrases.json'

def load_phrases():
    # Если файла нет, создаём его с пустой JSON-структурой
    if not os.path.exists(PHRASES_FILEPATH):
        with open(PHRASES_FILEPATH, "w", encoding="utf-8") as f:
            json.dump({}, f)
        return {}
    
    try:
        with open(PHRASES_FILEPATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Если файл есть, но пустой или битый — перезаписываем
        with open(PHRASES_FILEPATH, "w", encoding="utf-8") as f:
            json.dump({}, f)
        return {}
    
def save_phrases(json_data):
    """
    Сохраняет текст в файл. Если файл существует — дописывает в конец.
    """
    try:
        with open(PHRASES_FILEPATH, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Ошибка записи в {PHRASES_FILEPATH}: {e}")