#! /usr/bin/python3

from graph_tool.all import Graph, graph_tool, pagerank
import json

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
node_url = g.new_vp("string") #attaches the URL to the vertices. This is useful for displaying the URL

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

        if url not in vert_map:
            #add to map
            new_node = g.add_vertex()
            vert_map[url] = new_node
            node_url[new_node] = url

        # Iterate over the children and add them to the graph
        for child in item["child_nodes"]:
            assert isinstance(child, str), f"ERR: graph_manip.add_node() expected strings in `child_nodes`" 
            #if child not in graph yet, create a node
            if child not in vert_map:
                new_node = g.add_vertex()
                vert_map[child] = new_node
                node_url[new_node] = child

            # Create the required edge
            g.add_edge(vert_map[url], vert_map[child])

	# success
    return 0

#removes specified node and all connecting edges
def remove_node(url):
    if url in vert_map:
        g.remove_vertex(vert_map[url])
        vert_map.pop(url)
        return 0 #success
    return -1 #failure
    
    
#testing and driver code. Will ~not~ be used in the final product.
if __name__ == '__main__':
    payload = '[{"url":"www.google.com","child_nodes":["www.abc.com","www.def.com"]},{"url":"www.rpi.edu","child_nodes":["www.google.com","www.abc.com"]}]'

    add_node(payload)
    graph_tool.draw.graph_draw(
                    g, 
                    edge_pen_width=5,
                    vertex_text=node_url, 
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

    graph_tool.draw.graph_draw(
                    g, 
                    edge_pen_width=5,
                    vertex_text=node_url, 
                    vertex_aspect=1, 
                    vertex_text_position=1, 
                    vertex_text_color='black',
                    vertex_font_family='sans',
                    vertex_font_size=11,
                    vertex_color=None,
                    vertex_size=20,
                    output="delgraph.png"
    )
                
    print("Doing good")
