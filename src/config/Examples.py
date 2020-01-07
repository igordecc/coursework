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
    # networkx.draw(graph_x)
    # plt.show()
    return graph_x


def Example2():
    # modular graph
    # connected by IGOR GRAPH
    import networkx
    import matplotlib.pyplot as plt
    IGOR_graph = Example1()

    oscillators_number = 10
    reconnectionProbability = 0.15
    neighbours = 3
    m2 = 2  # must be even
    m1 = oscillators_number // 2 - m2 // 2

    graph_x = [
        networkx.scale_free_graph(oscillators_number),
        networkx.complete_graph(oscillators_number),
        networkx.fast_gnp_random_graph(oscillators_number, p=1),
        networkx.watts_strogatz_graph(oscillators_number, neighbours, reconnectionProbability),
        networkx.barbell_graph(m1, m2)
    ]

    print(graph_x[0].edges)
    networkx.draw(graph_x[0])
    plt.show()

if __name__ == '__main__':
    Example2()