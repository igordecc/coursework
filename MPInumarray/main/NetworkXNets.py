import networkx
from matplotlib import pyplot

osc_number = 100
neighbours = 4
connectionProb = 0.4
a = networkx.watts_strogatz_graph(osc_number, neighbours, connectionProb)
networkx.draw(a)
pyplot.show()
# for node, adj in c.adjacency():
#     print(node, "connected to", *tuple(adj.keys()))
##networkx.to_numpy_array(a)

# b = networkx.scale_free_graph(osc_number)
# networkx.draw(b)
# pyplot.show()
# print(networkx.to_numpy_array(b))
