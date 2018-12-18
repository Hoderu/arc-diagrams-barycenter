import matplotlib.pyplot as plt
from matplotlib.patches import Arc
import random
import argparse

plt.figure(figsize=(16, 16))
ax = plt.gca()

def makeGraph(n):
    random.seed()
    graph = [[random.randint(0, 1) for i in range(n)] for j in range(n)]
    for i in range(n):
        graph[i][i] = 0
    for i in range(n):
        for j in range(n):
            graph[j][i] = graph[i][j]
    return graph

def plot(graph, orderedNodes, inset):
    size = len(graph)

    numbersCoords = 0
    for i in range(0, size):
        plt.text(inset, numbersCoords, str(orderedNodes[i]['index']), color="red", fontsize=12)
        numbersCoords += 100

    for i in range(0, size):
        for j in range(0, i):
            if (graph[i][j] == 1):
                wh = positionOfNode(i, orderedNodes) - positionOfNode(j, orderedNodes)
                y = wh/2 + positionOfNode(j, orderedNodes)
                wh = abs(wh)
                arc_element = Arc((inset, y*100), wh*100, wh*100, angle=90.0, theta1=0.0, theta2=180, linewidth=0.4, zorder=0, color="k")
                ax.add_patch(arc_element)

def positionOfNode(i, orderedNodes):
    n = len(orderedNodes)
    for p in range(0, n):
        if (orderedNodes[p]['index'] == i):
            return p

def positionOfNodeCached(i, orderedNodes, nodes):
    N = len(orderedNodes)
    if (orderedNodes[ nodes[i].position ].index != i):
        # The cached position is not valid.
        # Update ALL the cached positions
        # so they will be valid next time.
        for p in range(0, N-1):
            nodes[ orderedNodes[p].index ].position = p
    return nodes[i].position

# compute average position of neighbors
def compute(graph, orderedNodes):
    N = len(graph)
    for _ in range(0,2*N):
        for i1 in range(0,N):
            p1 = positionOfNode(i1, orderedNodes)
            sum = p1
            neighborsLen = 0
            for j in range(0,N):
                if (i1 != j and graph[i1][j] == 1):
                    p2 = positionOfNode(j, orderedNodes)
                    sum = sum + p2
                    neighborsLen += 1
            orderedNodes[p1]['average'] = sum / (neighborsLen+1)
        # sort the array according to the values of average
        orderedNodes = sorted(orderedNodes, key=lambda k: k['average'])
    return orderedNodes

if __name__ == "__main__":
    ap = argparse.ArgumentParser()

    ap.add_argument("-v", "--vertices", required=True,
                    help="Count of vertices")
    args = vars(ap.parse_args())
    size = (int)(args['vertices'])
    if (size == 0):
        size = 14
    graph = makeGraph(size)

    orderedNodes = [{'index': i, 'average': 0} for i in range(size)]
    plot(graph, orderedNodes, -250 - size*50)
    orderedNodes = compute(graph, orderedNodes)
    plot(graph, orderedNodes, 750)

    plt.xlim(-1000 - size*100, 1000)
    plt.ylim(-100, 2000 + size*100)
    plt.show()



