from PriorityQueue import PriorityQueue

class SectorMap:
    def __init__(self, filename):
        with open(filename, "r") as f:
            contents = f.readlines()

        self.adjacency = {}
        for line in contents:
            self.read_corridor_line(line.strip())

    def read_corridor_line(self, line):
        line = line.split(" ")
        self.set_length(int(line[1]), int(line[2]), int(line[3]))

    def set_length(self, node_a, node_b, weight):
        self.one_directional_set_length(node_a, node_b, weight)
        self.one_directional_set_length(node_b, node_a, weight)

    def one_directional_set_length(self, node_a, node_b, weight):
        if node_a not in self.adjacency:
            self.adjacency[node_a] = {}
        self.adjacency[node_a][node_b] = weight

    def get_length(self, node_a, node_b):
        if node_a not in self.adjacency or node_b not in self.adjacency[node_a]:
            return None
        return self.adjacency[node_a][node_b]

    def jarnik(self):
        vertices = [list(self.adjacency.keys())[0]] # remember when building tests to test for the first element not being 1
        edges = []
        to_explore = [(vertices[0], n) for n in self.adjacency[vertices[0]]]

        while len(vertices) < len(self.adjacency): #case where one vertex is disconnected?
            lowest_edge = None
            lowest_weight = None
            for edge in to_explore:
                if (edge[1] not in vertices) and (lowest_weight == None or self.adjacency[edge[0]][edge[1]] < lowest_weight):
                    lowest_edge = edge
                    lowest_weight = self.adjacency[edge[0]][edge[1]]

            vertices.append(lowest_edge[1])
            edges.append(lowest_edge)

            for neighbor in self.adjacency[lowest_edge[1]]:
                neighbor = (lowest_edge[1], neighbor)
                if neighbor[::-1] not in to_explore:
                    to_explore.append(neighbor)

        return edges

    def trace_path(self, from_node, to_node, parents):
        path = []
        current = to_node
        while parents[current] != current:
            path.append(current)
            current = parents[current]
        path.append(parents[current])
        return path[::-1]

    def dijkstra(self, from_node, to_node):
        parents = {from_node: from_node}
        weights = {from_node: 0}

        frontier = PriorityQueue([[from_node, 0]])
        while len(frontier) > 0:
            current = frontier.pop()
            weight = weights[current]

            for neighbor in self.adjacency[current]:
                if (neighbor not in parents) or (weights[neighbor] > weight + self.adjacency[current][neighbor]):
                    weights[neighbor] = weight + self.adjacency[current][neighbor]
                    parents[neighbor] = current
                    frontier.push(neighbor, weights[neighbor])

                if neighbor == to_node:
                    return self.trace_path(from_node, to_node, parents)

        return None
