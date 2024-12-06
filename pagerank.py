# Using an example graph for now to test PageRank, will need to be replaced with our actual webgraph

from graph_tool.all import Graph, pagerank
from time import time

g = Graph()
url = g.new_vertex_property("string")

v1 = g.add_vertex()
url[v1] = "https://www.google.com"
v2 = g.add_vertex()
url[v2] = "https://www.youtube.com"
v3 = g.add_vertex()
url[v3] = "https://www.facebook.com"
v4 = g.add_vertex()
url[v4] = "https://cs.rpi.edu"

e1 = g.add_edge(v2,v1)
e2 = g.add_edge(v3,v1)
e3 = g.add_edge(v3,v4)
e4 = g.add_edge(v4,v1)

# can add mutexes around this function or something, if we don't want to lock the entire graph then
# we probably have to implement pagerank ourselves
start = time()
pr = pagerank(g)
print(f"PageRank time taken: {time()-start}")

print("Vertices:")
for v in g.vertices():
    print(f"Vertex {int(v)}: {url[v]}")

print("\nEdges:")
for e in g.edges():
    print(f"{url[e.source()]} to {url[e.target()]}")

print("\nPageRank scores:")
for v in g.vertices():
    print(f"{url[v]}: {pr[v]}")