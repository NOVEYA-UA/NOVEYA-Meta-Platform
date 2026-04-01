import os

class IdeaMatrix:
    def __init__(self):
        self.relations = {
            "R01": "Иерархичность", "R02": "Порождаемость", "R03": "Параллелизм",
            "R04": "Совместимость", "R05": "Антагонизм", "R06": "Цикличность",
            "R07": "Синхронность", "R08": "Вложенность", "R09": "Трансляция",
            "R10": "Эквивалентность", "R11": "Торможение", "R12": "Синтез"
        }
        self.priority_stack = [24, 11, 3, 1, 5] 
        self.medium_level_threshold = 0.50 

    def get_matrix_view(self, current_status):
        """Формирует текстовую визуализацию графа для Бота."""
        view = "📊 **МАТРИЦА ИДЕЙ: СОСТОЯНИЕ СЕТИ**\n\n"
        
        # Показываем очередь приоритетов
        view += "🔝 **Очередь приоритетов (Шаговый сдвиг):**\n"
        for i, sector in enumerate(self.priority_stack):
            prefix = "🔥" if i == 0 else "🔹"
            val = current_status.get(sector, 0) * 100
            view += f"{prefix} P{i+1}: Сектор {sector} [{val:.1f}%]\n"
        
        view += "\n🔗 **Активные бинарные отношения:**\n"
        # Пример: Связь Власти (24) и ЖКХ (11) через Порождаемость
        view += f"• 24 ➔ 11: {self.relations['R02']} (Порождаемость)\n"
        view += f"• 11 ➔ 5: {self.relations['R05']} (Антагонизм)\n"
        
        return view

    def calculate_step_shift(self, current_sector_status):
        current_p1 = self.priority_stack[0]
        status = current_sector_status.get(current_p1, 0)
        if status >= self.medium_level_threshold:
            moved_sector = self.priority_stack.pop(0)
            self.priority_stack.append(moved_sector)
            return True, moved_sector
        return False, current_p1

if __name__ == "__main__":
    matrix = IdeaMatrix()
    print(matrix.get_matrix_view({24: 0.45, 11: 0.12}))
