#    Licence

#    Copyright (C) 2004-2018 by
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Pieter Swart <swart@lanl.gov>
#    All rights reserved.
#    BSD license.

#    Copyright (C) 2004-2018 by
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Pieter Swart <swart@lanl.gov>
#    All rights reserved.
#    BSD license.
...
#https://en.wikipedia.org/wiki/Graph_property

import matplotlib.pyplot as plt
from networkx import nx

G = nx.lollipop_graph(4, 6)

pathlengths = []

print("nx.single_source_shortest_path_length ->> source vertex {target:length, }")
for v in G.nodes():
    spl = dict(nx.single_source_shortest_path_length(G, v))
    print('{} {} '.format(v, spl))
    for p in spl:
        pathlengths.append(spl[p])

print('')
print("average shortest path length %s" % (sum(pathlengths) / len(pathlengths)))

print("histogram of path lengths")
dist = {}
for p in pathlengths:
    if p in dist:
        dist[p] += 1
    else:
        dist[p] = 1

print('')
print("length #paths")
verts = dist.keys()
for d in sorted(verts):
    print('%s %d' % (d, dist[d]))

print("radius: %d" % nx.radius(G))
print("diameter: %d" % nx.diameter(G))
print("eccentricity: %s" % nx.eccentricity(G))
print("center: %s" % nx.center(G))
print("periphery: %s" % nx.periphery(G))
print("density: %s" % nx.density(G))

def notOrigin():

    print("Betweenness")
    b = nx.betweenness_centrality(G)
    for v in G.nodes():
        print("%0.2d %5.3f" % (v, b[v]))

    print("Degree centrality")
    d = nx.degree_centrality(G)
    for v in G.nodes():
        print("%0.2d %5.3f" % (v, d[v]))

    print("Closeness centrality")
    c = nx.closeness_centrality(G)
    for v in G.nodes():
        print("%0.2d %5.3f" % (v, c[v]))

notOrigin()

nx.draw(G, with_labels=True)
plt.show()