import logging

class SVET:
    def __init__(self):
        """Инициализация системы СВЕТ (Система Внутреннего Энергетического Течения)."""
        self.energy_level = 100
        self.harmony = True
        self.social_balance = 100
        self.ethical_justice = 100

    def balance(self, input_energy):
        """Функция балансировки энергетического потока."""
        if input_energy > 120:
            self.harmony = False
            logging.warning("⚠ Перегрузка! Система стабилизируется...")
            return "⚠ Перегрузка! Система стабилизируется..."
        elif input_energy < 80:
            self.harmony = False
            logging.warning("⚠ Энергии недостаточно. Активация резонанса...")
            return "⚠ Энергии недостаточно. Активация резонанса..."
        else:
            self.harmony = True
            logging.info("✅ Баланс энергии сохранён.")
            return "✅ Баланс энергии сохранён."

    def adjust_energy(self, change):
        """Изменение уровня энергии с учетом пределов."""
        self.energy_level += change
        self.energy_level = min(max(self.energy_level, 50), 150)
        return f"🔋 Энергетический уровень скорректирован: {self.energy_level}"

    def regulate_social_balance(self, impact):
        """Регулирование социального равновесия."""
        self.social_balance += impact
        self.social_balance = max(0, min(self.social_balance, 200))
        logging.info("👥 Социальный баланс скорректирован.")
        return "👥 Социальный баланс скорректирован."

    def regulate_ethical_justice(self, impact):
        """Регулирование этической справедливости."""
        self.ethical_justice += impact
        self.ethical_justice = max(0, min(self.ethical_justice, 200))
        logging.info("⚖️ Этическая справедливость обновлена.")
        return "⚖️ Этическая справедливость обновлена."

# Тестирование
if __name__ == "__main__":
    svet = SVET()
    print(svet.balance(130))
    print(svet.adjust_energy(-30))
    print(svet.regulate_social_balance(-10))
    print(svet.regulate_ethical_justice(15))
