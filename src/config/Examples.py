def Example0():
    import networkx
    import matplotlib.pyplot as plt

    x = [(i, i + 3) for i in range(10)]

    graph_x = networkx.Graph(x)
    networkx.draw(graph_x)
    plt.show()

def Example1():
    # IGOR GRAPH!
    # MIT LICENSE!
    # ALL RIGHTS (C)
    import networkx
    import matplotlib.pyplot as plt
    n = 10
    x = [(i, i+n) for i in range(n)]
    y = [(i+1, i+2) for i in range(n-1)] + [(1,n)]

    x += y
    graph_x = networkx.Graph(x)
    networkx.draw(graph_x)
    plt.show()

if __name__ == '__main__':
    Example1()