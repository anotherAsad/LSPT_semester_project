# Using an example graph for now to test PageRank, will need to be replaced with our actual webgraph

# TO DO: make an example graph with the data that we would be storing (url, outlinks, pagerank score, metadata)
#        test graph-tool's pagerank function on it and see if that works fine

from graph_tool.all import Graph, pagerank

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

pr = pagerank(g)

print("Vertices:")
for v in g.vertices():
    print(f"Vertex {int(v)}: {url[v]}")

print("\nEdges:")
for e in g.edges():
    print(f"{url[e.source()]} to {url[e.target()]}")

print("\nPageRank scores:")
for v in g.vertices():
    print(f"{url[v]}: {pr[v]}")