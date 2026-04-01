import json
import os

def authenticate_user(input_phrase):
    """Аутентификация пользователя на основе введённой фразы."""
    file_path = "users.json"

    # Проверка существования файла
    if not os.path.exists(file_path):
        return "Ошибка: база пользователей не найдена."

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            users = data.get("users", [])
    except json.JSONDecodeError:
        return "Ошибка: повреждённый файл пользователей."

    input_phrase_lower = input_phrase.lower()

    for user in users:
        if user["name"].lower() in input_phrase_lower:
            return f"✅ Доступ разрешён: {user['role']}"

    return "⛔ Ошибка: пользователь не найден."

# Пример вызова
if __name__ == "__main__":
    test_input = "Я, Татьяна Бондаренко, участник проекта НОВЕЯ."
    print(authenticate_user(test_input))
