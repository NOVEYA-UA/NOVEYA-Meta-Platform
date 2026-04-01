
class LearningModule:

    def update(self, zn_registry, result):
        # simple adaptive rule
        delta = 0.01 if result < 0.75 else -0.005
        for code in zn_registry.indicators:
            zn_registry.adjust_weights(code, delta)
