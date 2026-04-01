
class LieTensionAnalyzer:

    def __init__(self):
        self.history = []

    def evaluate(self, expected, actual):
        tension = 0
        for key in expected:
            if key in actual:
                diff = abs(expected[key] - sum(actual[key])/len(actual[key]))
                tension += diff
        self.history.append(tension)
        return tension

    def adapt(self, zn):
        if not self.history:
            return
        t = self.history[-1]
        for code in zn.indicators:
            if t > 0.2:
                zn.adjust_weights(code, 0.02)
            else:
                zn.adjust_weights(code, -0.005)
