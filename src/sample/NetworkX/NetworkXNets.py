import networkx
from matplotlib import pyplot

osc_number = 100
neighbours = 4
connectionProb = 0.4

# a = networkx.watts_strogatz_graph(osc_number, neighbours, connectionProb)
# networkx.draw(a)
# pyplot.show()

# b = networkx.scale_free_graph(osc_number)
# networkx.draw(b)
# pyplot.show()
# print(networkx.to_numpy_array(b))

# c = networkx.fast_gnp_random_graph(osc_number, connectionProb)
# networkx.draw(c)
# pyplot.show()
# print(networkx.to_numpy_array(c))

d = networkx.fast_gnp_random_graph(osc_number, p=1)
networkx.draw(d)
pyplot.show()
print(networkx.to_numpy_array(d))
