
class IdeaMatrix24:

    def __init__(self):
        self.sectors = {i: {} for i in range(1, 25)}

    def connect(self, a, b, relation):
        self.sectors[a][b] = relation
        self.sectors[b][a] = relation

    def get_relations(self, sector):
        return self.sectors.get(sector, {})

    def evaluate_path(self, start):
        visited = set()
        stack = [start]
        path = []

        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                path.append(node)
                stack.extend(self.sectors[node].keys())

        return path
