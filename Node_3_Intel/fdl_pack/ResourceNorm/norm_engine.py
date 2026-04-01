import os
import time

class FlowRegulator:
    def __init__(self):
        # Считываем путь из системного меридиана
        self.base_path = os.getenv('FDL_CORE', 'C:/Protonoveya-Noveya/FDL pack')
        self.flow_limit = 100  # Базовая норма Σ::Δ+::NORMA

    def regulate(self, task):
        """Регулятор потока Σ‑FDL с функцией конденсации."""
        try:
            current = task.get('current', 0)
            expected = task.get('expected', 1)
            diff = (current - expected) / expected * 100
            
            if diff > 0:
                # Вводим "сопротивление" (паузу) для нормализации
                wait_time = min(diff / 10, 5) 
                print(f"🌊 Поток: {current}. Избыток: {diff}%. Включаю конденсацию ({wait_time}s)...")
                time.sleep(wait_time)
                return f"⚠️ Норма Σ::Δ+::NORMA::{task['type']} скорректирована. Избыток поглощен."
            
            return f"✅ Норма Σ::Δ+::NORMA::{task['type']} в резонансе."
        except Exception as e:
            return f"🌀 Шум в регуляторе: {e}"

if __name__ == "__main__":
    reg = FlowRegulator()
    # Тестовый импульс с перегрузкой
    task = {'type': 'FLOW', 'current': 150, 'expected': 100}
    print(reg.regulate(task))
