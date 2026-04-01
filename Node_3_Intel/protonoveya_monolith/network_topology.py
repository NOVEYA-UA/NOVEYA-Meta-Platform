import psutil

class OSTopology:
    def snapshot(self):
        nodes = []
        edges = []

        for proc in psutil.process_iter(['pid', 'ppid', 'name']):
            nodes.append(proc.info)
            edges.append({"from": proc.info['ppid'], "to": proc.info['pid']})

        return {"nodes": nodes, "edges": edges}