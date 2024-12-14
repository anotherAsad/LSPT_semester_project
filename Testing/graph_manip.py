#! /usr/bin/python3

from graph_tool.all import Graph, graph_tool, find_vertex, pagerank
import threading
import json


'''
example payload:
{
    "url":"www.example.com",
    "child_nodes":["www.abc.com", "www.def.com"]
}
'''

# Mutex for graph update

#create Graph as global so it is accessible everywhere
g = Graph(directed=True)
graph_update_mutex = threading.Lock()

# graph properties
node_url = g.new_vp("string") # attaches the URL to the vertices. This is useful for displaying the URL
page_rank = None
node_text = g.new_vp("string")
click_count = g.new_vp("int")


# returns the vertex
def find_in_graph(url):
    list_of_nodes = find_vertex(g, node_url, url)

    if len(list_of_nodes) != 1:
        return None
    else:
        return list_of_nodes[0]

#adds specified node and connects it to children.
#also adds edges between existing nodes and creates nodes that aren't there.
#can create multiple nodes at once as long as the JSON is formatted like:
'''
[
    {
        "url":"www.example.com",
        "child_nodes":["www.abc.com", "www.def.com"]
    },
    {
        "url":"www.rpi.edu",
        "child_nodes":["www.def.com"]
    },
    
    ...
    
]

'''

# Adds a node and its children from the json. Doesn't perform redundant addition of edges and nodes.
def add_nodes(payload):
    payload_list = json.loads(payload)

    # Handle both a single payload or a list of payloads
    if isinstance(payload_list, dict):                      # if a single payload (as a dict) is found, convert it into a list.
        payload_list = [payload_list]
    else:                                                   # if the payload was not a dict, it must be a list
        try:
            assert isinstance(payload_list, list)
        except Exception as e:
            print(f"\tERR: graph_manip.add_node() expected `payload_list` as list or a sigle dict")
            return -1
    
    # iterate over item tuples (url, child_nodes) and add them to graph
    for item in payload_list:
        # Check if the item is a dictionary.
        try:
            assert isinstance(item, dict)
        except Exception as e:
            print("\tERR: graph_manip.add_node() expected `item` as dictionary")
            return -1

        url = item["url"]

        try:
            assert isinstance(url, str)
        except Exception as e:
            print("\tERR: graph_manip.add_node() expected `url` as string")
            return -1

        # get node from url
        parent_node = find_in_graph(url)

        if parent_node == None:
            #add to graph
            parent_node = g.add_vertex()
            node_url[parent_node] = url
            click_count[parent_node] = 0

        # case of stray node with no children
        if not "child_nodes" in item:
            continue

        try:
            assert isinstance(item["child_nodes"], list)
        except Exception as e:
            print("""\tERR: graph_manip.add_node() expected `item["child_nodes"]` as list""")
            return -1

        # Iterate over the children and add them to the graph
        for child in item["child_nodes"]:
            try:
                isinstance(child, str)
            except Exception as e:
                print("\tERR: graph_manip.add_node() expected strings in `child_nodes`" )
                return -1

            #if child not in graph yet, create a node
            child_node = find_in_graph(child)

            if child_node == None:
                child_node = g.add_vertex()
                node_url[child_node] = child
                click_count[child_node] = 0

            # Create the required edge
            if not g.edge(parent_node, child_node):
                g.add_edge(parent_node, child_node)

	# success
    return 0

# removes specified node and all connecting edges
def remove_node(url):
    node = find_in_graph(url)

    if node != None:
        g.remove_vertex(node)
        return True #success

    return False #failure

# Adds click count info to the graph
def update_metadata(payload):
    if len(payload.list_of_clicked_links) != len(payload.click_count):
        print(f"ERR: graph_manip.update_metadata() expected equal list lengths")
        return False

    for idx in range(len(payload.list_of_clicked_links)):
        node = find_in_graph(payload.list_of_clicked_links[idx])

        if node != None:
            click_count[node] += payload.click_count[idx]

    return True

    # TODO: Write actual code
    return True
    
# converts the graph to json
def convert_graph_to_JSON(g):
    graph_data = {
        "nodes": [{"id": int(v), "url": node_url[v], "page_rank": page_rank[v], "click_count": click_count[v]} for v in g.vertices()],
        "edges": [{"source": int(e.source()), "target": int(e.target())} for e in g.edges()]
    }

    return graph_data

# converts the subgraph to json
def convert_subgraph_to_JSON(subg, prop, pg, ck):
    graph_data = {
        "nodes": [{"id": int(v), "url": prop[v], "page_rank": pg[v], "click_count": ck[v]} for v in g.vertices()],
        "edges": [{"source": int(e.source()), "target": int(e.target())} for e in g.edges()]
    }
    
    return graph_data
    
# extract a subgraph from the bigger mother graph
def get_subgraph(base_url, n):
    visited = set()
    
    base = find_in_graph(base_url)

    if base == None:
        return None, None, None, None

    queue = [(base, 0)]
    
    res = Graph()
    urls = res.new_vp("string")
    rank = res.new_vp("float")
    clik = res.new_vp("string")
    parent = None
    
    while queue:
        v, d = queue.pop(0)
        if v not in visited and d <= n:
            visited.add(v)
            #add new vector to subgraph and set property
            new_v = res.add_vertex()
            if parent:
                res.add_edge(parent, new_v)
            urls[new_v] = node_url[v]
            rank[new_v] = page_rank[v]
            clik[new_v] = click_count[v]

            for child in g.get_out_neighbors(v):
                queue.append((child, d + 1))
                parent = new_v
    
    return res, urls, rank, clik


# DESCRIPTION: prints the graph as a PNG
def visualize_graph(filename):
    assert isinstance(filename, str), f"ERR: graph_manip.add_node() expected `filename` as string"

    if g.num_vertices() == 0:
        return False

    graph_update_mutex.acquire()		# acquire mutex lock

    # update the text that is to be shown in graph visualization
    for node in g.vertices():
        node_text[node] = f"{node_url[node]}: {page_rank[node]:.3f}"

    graph_tool.draw.graph_draw(
        g,
        bg_color=[1,1,1,1],
        edge_pen_width=5,
        vertex_text=node_text, 
        vertex_aspect=1, 
        vertex_text_position=1, 
        vertex_text_color='black',
        vertex_font_family='sans',
        vertex_font_size=11,
        vertex_color=None,
        vertex_size=20,
        output=filename
    )

    graph_update_mutex.release()		# release mutex lock

    return True

#testing and driver code. Will ~not~ be used in the final product.
if __name__ == '__main__':
    payload = '[{"url":"www.google.com","child_nodes":["www.abc.com","www.def.com"]},{"url":"www.rpi.edu","child_nodes":["www.google.com","www.abc.com"]}]'

    add_node(payload)

    visualize_graph("mygraph.png")

    remove_node("www.abc.com")

    visualize_graph("delgraph.png")