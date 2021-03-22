class Graph:
    def __init__(self, matrix=None) -> None:
        self.nodes = []
        self.edges = []
        if matrix != None:
            tmp_matrix = matrix.copy()
            node = 'node'
            wall = 'wall'
            water = 'water'
            for i in range(len(matrix)):
                for j in range(len(matrix[i])):

                    pos = '_'+str(i)+'_'+str(j)
                    label = wall+pos
                    n = Node()
                    n.value = label
                    if matrix[i][j] == 'start':
                        label = node+pos
                        n.value = label
                        self.start_node = n
                    elif matrix[i][j] == 'end':
                        label = node+pos
                        n.value = label
                        self.end_node = n
                    elif matrix[i][j] == 'node':
                        label = node+pos
                        n.value = label
                    elif matrix[i][j] == 'water':
                        label = water+pos
                        n.value = label
                    self.nodes.append(n)
                    tmp_matrix[i][j] = n

            offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            for i in range(len(matrix)):
                for j in range(len(matrix[i])):
                    current = tmp_matrix[i][j]
                    for offset in offsets:
                        if i+offset[0] == -1 or j+offset[1] == -1:
                            continue
                        try:
                            neighbour = tmp_matrix[i+offset[0]][j+offset[1]]
                        except IndexError:
                            continue

                        cost = 1
                        if neighbour.value.split('_')[0] == 'water':
                            cost = 1000000
                        if neighbour.value.split('_')[0] != 'wall':
                            self.edges.append(Edge(current, neighbour, cost))

    def add_node(self, node):
        self.nodes.append(node)

    def add_edge(self, edge):
        self.edges.append(edge)


class Node:
    def __init__(self, value=None):
        self.value = value

    def __eq__(self, other):
        return self.value == other.value if type(other) == Node else False

    def __repr__(self):
        return str(self.value)

    def __str__(self):
        return str(self.value)


class Edge:
    def __init__(self, n1, n2, cost=0):
        self.n1 = n1
        self.n2 = n2
        self.cost = cost

    def __eq__(self, other):
        return self.n1 == other.n1 and self.n2 == other.n2 and self.cost == other.cost

    def __repr__(self):
        return str(self.n1)+' '+str(self.n2)+str(self.cost)

    def __str__(self):
        return str(self.n1)+' '+str(self.n2)+str(self.cost)
