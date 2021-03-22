from math import sqrt


def distance(p, G):
    x1, y1 = p[-1].value.split('_')[1:]
    x1, y1 = int(x1), int(y1)
    x2, y2 = G.end_node.value.split('_')[1:]
    x2, y2 = int(y1), int(y2)

    return sqrt(pow((x1-x2), 2)+pow(y1-y2, 2))
