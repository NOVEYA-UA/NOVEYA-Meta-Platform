
class RankEvaluator:

    def __init__(self):
        self.functions = {}
        self.priorities = {}

    def add_function(self, name, func, priority):
        self.functions[name] = func
        self.priorities[name] = priority

    def evaluate(self, inputs):
        return sum(
            self.functions[k](inputs[k]) * self.priorities[k]
            for k in self.functions
        )
