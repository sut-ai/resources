class Graph:
    def __init__(self, n: int):
        self.n = n
        self.is_known = [False] * n
        self.neighbors = {}
        self.discovered = [False] * n
        for i in range(n):
            self.neighbors[i] = []

    def add_neighbor(self, start: int, end: int):
        if end not in self.neighbors[start - 1]:
            self.neighbors[start - 1].append(end - 1)

    def make_known(self, nodes: list):
        for node in nodes:
            self.is_known[node] = True

    def make_all_unknown(self):
        self.is_known = [False] * n

    # checks activity of whole path
    def check_active(self, path) -> bool:
        for i in range(len(path) - 2):
            if self.check_triplet(path[i:i + 3]):
                return False
        return True

    # checks inactivity of a triplet
    def check_triplet(self, triplet) -> bool:
        triplet_type = self.get_triplet_type(triplet)
        if triplet_type % 2 == 1:
            if self.is_known[triplet[1] - 1]:
                return True
            return False
        if self.is_known[triplet[1] - 1]:
            return False
        if self.has_known_descendant(triplet[1] - 1):
            return False
        return True

    # DFS to find a known child or grandchild
    def has_known_descendant(self, node) -> bool:
        stack = [node]
        while len(stack) > 0:
            v = stack.pop(0)
            if not self.discovered[v]:
                if self.is_known[v]:
                    return True
                self.discovered[v] = True
                for nei in self.neighbors[v]:
                    stack.append(nei)
        self.discovered = [False] * self.n
        return False

    # type 1 is o>o>o, 3 is o<o>o, 2 is o>o<o
    def get_triplet_type(self, triplet) -> int:
        edges = [0 if triplet[1] - 1 in self.neighbors[triplet[0] - 1] else 1,
                 0 if triplet[2] - 1 in self.neighbors[triplet[1] - 1] else 1]
        if sum(edges) % 2 == 0:
            return 1
        if edges[0] == 0:
            return 2
        return 3


if __name__ == "__main__":
    n, m = map(int, input().split())
    graph = Graph(n)
    for _ in range(m):
        x, y = map(int, input().split())
        graph.add_neighbor(x, y)
    q = int(input())
    for _ in range(q):
        path = list(map(int, input().split()))
        known = input().split()
        if known[0] != 'none':
            graph.make_known([int(i) - 1 for i in known])
        if graph.check_active(path):
            print("active")
        else:
            print("inactive")
        graph.make_all_unknown()
