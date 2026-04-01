
import time
from zn_indicator_registry import ZnRegistry
from rank_evaluator import RankEvaluator
from lie_analyzer import LieTensionAnalyzer
from meridian_sync import MeridianSync
from idea_matrix import IdeaMatrix24

class ServiceRegulator:

    def __init__(self):
        self.zn = ZnRegistry()
        self.rank = RankEvaluator()
        self.lie = LieTensionAnalyzer()
        self.sync = MeridianSync("Protonoveya_Zn")
        self.matrix = IdeaMatrix24()
        self.last_result = 0

        self.zn.add_indicator("EFFICIENCY",
            ("quality","time","stability"),
            (0.5,0.3,0.2))

        self.rank.add_function(
            "EFFICIENCY",
            lambda x: self.zn.evaluate("EFFICIENCY", x),
            1.0
        )

        # Example relations
        self.matrix.connect(1,2,"influence")
        self.matrix.connect(2,3,"dependency")

    def run_cycle(self):
        data = self.sync.fetch()

        result = self.rank.evaluate(data)
        self.last_result = result

        tension = self.lie.evaluate(
            {"EFFICIENCY": result},
            data
        )

        self.lie.adapt(self.zn)

        self.sync.write(result)

        print("R:", result, "T:", tension)

    def run(self):
        while True:
            self.run_cycle()
            time.sleep(60)

if __name__ == "__main__":
    ServiceRegulator().run()
