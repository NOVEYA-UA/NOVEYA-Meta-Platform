class FDL_Logic:
    def __init__(self, thesis, antithesis):
        self.thesis = thesis
        self.antithesis = antithesis
        self.synthesis = None
        self.pragmatics = None

    def synthesize(self):
        """Выполняет синтез тезиса и антитезиса."""
        self.synthesis = f"Синтез: {self.thesis} + {self.antithesis} → Новая идея"
        return self.synthesis

    def pragmatize(self):
        """Формирует прагматический вывод на основе синтеза."""
        if self.synthesis:
            self.pragmatics = f"Оптимальное решение: {self.synthesis}"
        else:
            self.pragmatics = "Сначала необходимо выполнить синтез."
        return self.pragmatics

class SVET:
    def __init__(self):
        self.energy_level = 100
        self.harmony = True
        self.social_balance = 100
        self.ethical_justice = 100

    def balance(self, input_energy):
        if input_energy > 120:
            self.harmony = False
            return "Перегрузка! Система стабилизируется..."
        elif input_energy < 80:
            self.harmony = False
            return "Энергии недостаточно. Активация резонанса..."
        else:
            self.harmony = True
            return "Баланс энергии сохранён."

class PranoveaInterpreter:
    def __init__(self):
        self.variables = {}
        self.svet = SVET()
        self.logic = None

    def execute(self, code):
        """Исполняет последовательность команд на языке осознания."""
        print("\nНачальное состояние СВЕТ:", self.svet.__dict__)
        lines = code.split("\n")
        for line in lines:
            line = line.strip()
            if line.startswith("тезис"):
                self.handle_thesis(line)
            elif line.startswith("антитезис"):
                self.handle_antithesis(line)
            elif line.startswith("синтез"):
                self.handle_synthesis()
            elif line.startswith("баланс"):
                self.handle_balance(line)
        print("\nКонечное состояние СВЕТ:", self.svet.__dict__)

    def handle_thesis(self, line):
        self.logic = FDL_Logic(line.replace("тезис ", ""), "")

    def handle_antithesis(self, line):
        if self.logic:
            self.logic.antithesis = line.replace("антитезис ", "")

    def handle_synthesis(self):
        if self.logic:
            print(self.logic.synthesize())

    def handle_balance(self, line):
        energy = int(line.replace("баланс ", ""))
        print(self.svet.balance(energy))

# Тестовый запуск
code = """
тезис "Общество должно развиваться гармонично"
антитезис "Избыточные блага могут привести к дисбалансу"
синтез
баланс 130
"""

interpreter = PranoveaInterpreter()
interpreter.execute(code)