import random


class Path:
    def __init__(self):
        self.p = []
        self.c = None

    def add_edge(self, edge):
        self.p.append(edge.n2)
        self.c += edge.cost


# Random choice of next path has high cost
def naive_search(G, S, goal):
    closed_list = []
    frontier = []
    for start in S:
        frontier.append([start])

    while len(frontier) != 0:
        index = random.randint(0, len(frontier)-1)
        path = frontier[index]
        del frontier[index]
        if path[-1] in closed_list:
            continue
        else:
            closed_list.append(path[-1])
        if goal(path[-1]):
            return path
        for edge in G.edges:
            if edge.n1 == path[-1] and not edge.n2 in path:
                new_path = path.copy()
                new_path.append(edge.n2)
                frontier.append(new_path)

    return []


# the frontier is a queue
# space and time complexity are exponential on the number of edges of the
# shortest path (which is certain to be found)
# useful when there aren't space problems
def breadth_first_search(G, S, goal):
    closed_list = []
    frontier = []
    for start in S:
        frontier.append([start])

    while len(frontier) != 0:
        path = frontier[0]
        del frontier[0]
        if path[-1] in closed_list:
            continue
        else:
            closed_list.append(path[-1])
        if goal(path[-1]):
            return path
        for edge in G.edges:
            if edge.n1 == path[-1] and not edge.n2 in path:
                new_path = path.copy()
                new_path.append(edge.n2)
                frontier.append(new_path)

    return []


# frontier is a stack
# linear in space, linear in time in the length of the path if it is found in the first branch
# else in the worst case if it's an infiite graph, diverges, else exponential
# useful if space is limited and there are multiple solutions
def depth_first_search(G, S, goal):
    closed_list = []
    frontier = []
    for start in S:
        frontier.append([start])

    while len(frontier) != 0:
        path = frontier[-1]
        del frontier[-1]
        if path[-1] in closed_list:
            continue
        else:
            closed_list.append(path[-1])
        if goal(path[-1]):
            return path
        for edge in G.edges:
            if edge.n1 == path[-1] and not edge.n2 in path:
                new_path = path.copy()
                new_path.append(edge.n2)
                frontier.append(new_path)

    return []


# Iterative version of iterative deepening
def it_iterative_deepening(G, S, goal):
    def depth_bounded_dfs(goal, b):
        closed_list = []
        max_len = 0
        frontier = []
        for start in S:
            frontier.append([start])

        while len(frontier) != 0:
            path = frontier[-1]
            del frontier[-1]
            if path[-1] in closed_list:
                continue
            else:
                closed_list.append(path[-1])
            tmp_len = len(path)
            if tmp_len > max_len:
                max_len = tmp_len
            if goal(path[-1]):
                return path
            elif tmp_len == b:
                continue
            else:
                for edge in G.edges:
                    if edge.n1 == path[-1] and not edge.n2 in path:
                        new_path = path.copy()
                        new_path.append(edge.n2)
                        frontier.append(new_path)
        if max_len < b:
            return -1
        return []

    bound = 1
    while True:
        path = depth_bounded_dfs(goal, bound)
        if path == -1:
            break
        elif path != []:
            return path
        bound += 1
    return []


# recursive version of iterative deepening
# fails naturally if searches the whole spaces, innaturally if hits bound
def rec_iterative_deepening(G, S, goal):
    def depth_bounded_search(path, b):
        if b > 0:
            for edge in G.edges:
                if edge.n1 == path[-1] and not edge.n2 in path:
                    tmp_path = path.copy()
                    tmp_path.append(edge.n2)
                    res = depth_bounded_search(tmp_path, b-1)
                    if type(res) == list:
                        return res
        elif goal(path[-1]):
            return path
        else:
            for edge in G.edges:
                if edge.n1 == path[-1]:
                    return
            return 'natural'

    bound = 0
    while True:
        for start in S:
            res = depth_bounded_search([start], bound)
            if type(res) == list:
                return res
            elif res == 'natural':
                return []
        bound += 1


# Frontier is ordered by the cost of the edge
def uniform_cost_search(G, S, goal):
    def ordered_insert(frontier, path):
        i = 0
        while i < len(frontier):
            if frontier[i].c < path.c:
                i += 1
            else:
                break
        frontier.insert(i, path)
        return frontier

    closed_list = []
    frontier = []
    for start in S:
        path = Path()
        path.p = [start]
        path.c = 0
        frontier.append(path)

    while len(frontier) != 0:
        path = frontier[0]
        del frontier[0]
        if path.p[-1] in closed_list:
            continue
        else:
            closed_list.append(path.p[-1])
        if goal(path.p[-1]):
            return path.p
        for edge in G.edges:
            if edge.n1 == path.p[-1] and not edge.n2 in path.p:
                new_path = Path()
                new_path.p = path.p.copy()
                new_path.c = path.c
                new_path.add_edge(edge)
                frontier = ordered_insert(frontier, new_path)

    return []


# A star algorithm
def A_star(G, S, goal, h):
    def ordered_insert(frontier, path):
        i = 0
        while i < len(frontier):
            if frontier[i].c + h(frontier[i].p, G) < path.c + h(path.p, G):
                i += 1
            else:
                break
        frontier.insert(i, path)
        return frontier

    closed_list = []
    frontier = []
    for start in S:
        path = Path()
        path.p = [start]
        path.c = 0
        frontier.append(path)

    while len(frontier) != 0:
        path = frontier[0]
        del frontier[0]
        if path.p[-1] in closed_list:
            continue
        else:
            closed_list.append(path.p[-1])
        if goal(path.p[-1]):
            return path.p
        for edge in G.edges:
            if edge.n1 == path.p[-1] and not edge.n2 in path.p:
                new_path = Path()
                new_path.p = path.p.copy()
                new_path.c = path.c
                new_path.add_edge(edge)
                frontier = ordered_insert(frontier, new_path)

    return []
