import graph_manip as gm

"""
Tests:
- Empty webgraph
- Webgraph with nodes

- Node in graph
- Node not in graph
- Other weird inputs (None, numbers, anything that isn't a string)
"""

def node_in_graph_test(url, expected_result):
    print(f"find_in_graph({url}): expected = {expected_result}, actual = ", end="")
    v = gm.find_in_graph(url)
    if v == None or gm.node_url[v] != url:
        print("not in graph")
    else:
        print("in graph")

print("Empty webgraph:")
for i in range(1,11):
    node_in_graph_test(str(i), "not in graph")
# node_in_graph_test(None, "not in graph") -> error
# node_in_graph_test(1, "not in graph") -> error

for i in range(1,11):
    v = gm.g.add_vertex()
    gm.node_url[v] = str(i)
    gm.click_count[v] = 0

print("\nWebgraph with only nodes:")
for i in range(1,11):
    node_in_graph_test(str(i), "in graph")
for i in range(11,20):
    node_in_graph_test(str(i), "not in graph")

gm.g.clear()

for i in range(1,11):
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

print("\nWebgraph with nodes and edges:")
for i in range(1,11):
    node_in_graph_test(str(i), "in graph")
for i in range(11,20):
    node_in_graph_test(str(i), "not in graph")