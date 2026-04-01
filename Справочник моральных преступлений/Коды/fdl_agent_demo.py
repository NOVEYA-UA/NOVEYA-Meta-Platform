from fdl_kernel import FDLAgent

# Инициализация агента с контекстом
agent = FDLAgent(context="Пример: размышление о силе и порядке")

# Входной запрос
input_query = "Решения силой — единственный путь к порядку."

# Получение ответа
response = agent.respond(input_query)

# Вывод
print("Запрос:", input_query)
print("Ответ агента:", response)