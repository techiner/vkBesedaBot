import os
import json
import re

PHRASES_FILENAME = 'phrases.json'

def load_phrases():
    # Если файла нет, создаём его с пустой JSON-структурой
    if not os.path.exists(PHRASES_FILENAME):
        with open(PHRASES_FILENAME, "w", encoding="utf-8") as f:
            json.dump({}, f)
        return {}
    
    try:
        with open(PHRASES_FILENAME, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Если файл есть, но пустой или битый — перезаписываем
        with open(PHRASES_FILENAME, "w", encoding="utf-8") as f:
            json.dump({}, f)
        return {}
    
def save_phrases(json_data):
    """
    Сохраняет текст в файл. Если файл существует — дописывает в конец.
    """
    try:
        with open(PHRASES_FILENAME, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Ошибка записи в {PHRASES_FILENAME}: {e}")

def find_phrase(text, phrase_database):
    """Поиск фразы без учета регистра"""
    res = []
    for key, value in phrase_database.items():
        pattern = r'(?<!\w)' + re.escape(key) + r'(?!\w)'
        if re.search(pattern, text, flags=re.IGNORECASE):
            res.append(value)

    if len(res) > 0:
        return " ".join(res)
    return None