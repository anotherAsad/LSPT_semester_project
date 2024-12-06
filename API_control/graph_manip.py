#! /usr/bin/python3

from graph_tool.all import Graph, graph_tool, find_vertex, pagerank
import threading
import json

update_mutex = threading.Lock()

'''
example payload:
{
    [
        "url": "www.google.com",
        "child_nodes": [
          "abc.com",
          "def.com"
        ]
    ]   

}

'''

#create Graph as global so it is accessible everywhere
g = Graph(directed=True)
vert_map = dict() #dict of ["URL": vertex_index]. This is so I can search the indices by url in less than O(N)
node_url = g.new_vp("string") # attaches the URL to the vertices. This is useful for displaying the URL
page_rank = None
node_text = g.new_vp("string")

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

def add_node(payload):
    payload_list = json.loads(payload)

    # Handle both a single payload or a list of payloads
    if isinstance(payload_list, dict):                      # if a single payload (as a dict) is found, convert it into a list.
        payload_list = [payload_list]
    else:                                                   # if the payload was not a dict, it must be a list
        assert isinstance(payload_list, list), f"ERR: graph_manip.add_node() expected `payload_list` as list or a sigle dict"
    
    # iterate over item tuples (url, child_nodes) and add them to graph
    for item in payload_list:
        # Check if the item is a dictionary
        assert isinstance(item, dict), f"ERR: graph_manip.add_node() expected `item` as dictionary"

        url = item["url"]
        assert isinstance(url, str), f"ERR: graph_manip.add_node() expected `url` as string"

        # get node from url
        parent_node = find_in_graph(url)

        if parent_node == None:
            #add to graph
            parent_node = g.add_vertex()
            node_url[parent_node] = url

        # Iterate over the children and add them to the graph
        for child in item["child_nodes"]:
            assert isinstance(child, str), f"ERR: graph_manip.add_node() expected strings in `child_nodes`" 
            #if child not in graph yet, create a node
            child_node = find_in_graph(child)

            if child_node == None:
                child_node = g.add_vertex()
                node_url[child_node] = child

            # Create the required edge
            g.add_edge(parent_node, child_node)

	# success
    return 0

#removes specified node and all connecting edges
def remove_node(url):
    node = find_in_graph(url)

    if node != None:
        g.remove_vertex(node)
        return 0 #success

    return -1 #failure
    
# converts the graph to json
def convert_graph_to_JSON(g):
    graph_data = {
        "nodes": [{"id": int(v)} for v in g.vertices()],
        "edges": [{"source": int(e.source()), "target": int(e.target())} for e in g.edges()]
    }

    return graph_data
    
#testing and driver code. Will ~not~ be used in the final product.
if __name__ == '__main__':
    payload = '[{"url":"www.google.com","child_nodes":["www.abc.com","www.def.com"]},{"url":"www.rpi.edu","child_nodes":["www.google.com","www.abc.com"]}]'

    add_node(payload)

    graph_manip.graph_tool.draw.graph_draw(
        graph_manip.g, 
        edge_pen_width=5,
        vertex_text=graph_manip.node_text, 
        vertex_aspect=1, 
        vertex_text_position=1, 
        vertex_text_color='black',
        vertex_font_family='sans',
        vertex_font_size=11,
        vertex_color=None,
        vertex_size=20,
        output="mygraph.png"
    )

    remove_node("www.abc.com")

    graph_manip.graph_tool.draw.graph_draw(
        graph_manip.g, 
        edge_pen_width=5,
        vertex_text=graph_manip.node_text, 
        vertex_aspect=1, 
        vertex_text_position=1, 
        vertex_text_color='black',
        vertex_font_family='sans',
        vertex_font_size=11,
        vertex_color=None,
        vertex_size=20,
        output="mygraph.png"
    )
                
    print("Doing good")
