import graph_manip as gm

"""
Tests:
- Empty webgraph
- Webgraph with nodes
- Webgraph with nodes and edges

- Node in graph
- Node not in graph
"""

def print_graph():
    print("  Vertices: ", end="")
    for v in gm.g.vertices():
        print(f"{gm.node_url[v]} | ", end="")
    print()
    print("  Edges: ", end="")
    for s,t in gm.g.iter_edges():
        print(f"{gm.node_url[s]} -> {gm.node_url[t]} | ", end="")
    print()

def remove_node_test(url, expected_result):
    print(f"remove_node({url}): expected = {expected_result}, actual = {gm.remove_node(url)}")
    print_graph()

print("Empty webgraph:")
for i in range(0,5):
    remove_node_test(str(i), False)

for i in range(0,5):
    v = gm.g.add_vertex()
    gm.node_url[v] = str(i)
    gm.click_count[v] = 0

print("\nWebgraph with only nodes:")
print_graph()
for i in range(0,5):
    remove_node_test(str(i), True)

print("Reset graph")
gm.g.clear()
for i in range(0,5):
    v = gm.g.add_vertex()
    gm.node_url[v] = str(i)
    gm.click_count[v] = 0

print_graph()
for i in range(5,10):
    remove_node_test(str(i), False)

gm.g.clear()

for i in range(0,3):
    v = gm.g.add_vertex()
    gm.node_url[v] = str(i)
    gm.click_count[v] = 0
for v1 in gm.g.vertices():
    for v2 in gm.g.vertices():
        if v1 != v2:
            gm.g.add_edge(v1,v2)

print("\nWebgraph with nodes and edges:")
print_graph()
for i in range(0,3):
    remove_node_test(str(i), True)

print("Reset graph")
gm.g.clear()
for i in range(0,3):
    v = gm.g.add_vertex()
    gm.node_url[v] = str(i)
    gm.click_count[v] = 0
for v1 in gm.g.vertices():
    count = 0
    for v2 in gm.g.vertices():
        if count == 5:
            break
        if v1 != v2:
            gm.g.add_edge(v1,v2)

print_graph();
for i in range(5,10):
    remove_node_test(str(i), False)
