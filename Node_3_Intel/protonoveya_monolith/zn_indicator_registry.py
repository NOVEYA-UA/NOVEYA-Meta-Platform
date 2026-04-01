
class ZnRegistry:

    def __init__(self):
        self.indicators = {}

    def add_indicator(self, code, parts, weights):
        self.indicators[code] = {
            "parts": parts,
            "weights": list(weights)
        }

    def evaluate(self, code, values):
        w = self.indicators[code]["weights"]
        return sum(v * w[i] for i,v in enumerate(values))

    def adjust_weights(self, code, delta):
        w = self.indicators[code]["weights"]
        for i in range(len(w)):
            w[i] += delta*(0.5 - w[i])
