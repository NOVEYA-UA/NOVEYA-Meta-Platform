import os
import datetime

class LieAnalyzer:
    """
    Ω-уровень: Автоматический перевод смыслов Ворда в фильтры управления.
    Реализует Постулат КАЕ: Оценка только в ОТНОСИТЕЛЬНЫХ ФОРМАХ.
    """
    def __init__(self):
        self.log_path = r"C:\Protonoveya-Noveya\protonoveya_monolith\Logs\system.log"
        # "Десятина" - критический порог отклонения (10%)
        self.tithe_threshold = 0.10 

    def log_event(self, message):
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")

    def evaluate_resource_logic(self, absolute_gain, relative_quality_loss):
        """
        Метод 'Вытаскивания' закона из файла 'формулы нормирования'.
        absolute_gain: например, сэкономленный газ (кубы).
        relative_quality_loss: падение качества жизни (индекс).
        """
        # Если экономия (Gain) ведет к падению качества больше чем на "десятину" (10%)
        if relative_quality_loss > self.tithe_threshold:
            report = (f"🚨 МОРАЛЬНОЕ ПРЕСТУПЛЕНИЕ №1: Скрытый вред под видом экономии. "
                      f"Абсолютный выигрыш ({absolute_gain}) перекрыт системным ущербом ({relative_quality_loss*100}%).")
            self.log_event(report)
            return report, False
        
        return "✅ Резонанс соблюден. Экономия допустима.", True

    def check(self, data_packet):
        """
        Главный фильтр Ω. 
        Сверяет импульс из Таблицы со Справочником преступлений.
        """
        gain = data_packet.get("resource_gain", 0)
        loss = data_packet.get("quality_drop", 0)
        
        verdict, is_legal = self.evaluate_resource_logic(gain, loss)
        
        if not is_legal:
            return f"❌ БЛОКИРОВКА СИНТЕЗА: {verdict}"
        return f"🟢 ИМПУЛЬС ПРИНЯТ: {verdict}"

if __name__ == "__main__":
    analyzer = LieAnalyzer()
    # Тест: Сэкономили 1000 кубов, но дети стали болеть на 15% чаще (больше десятины)
    print(analyzer.check({"resource_gain": 1000, "quality_drop": 0.15}))
