from graph_tool.all import *
import json

'''
example payload:
{
    [
        "url": "www.google.com"
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
prop_vp = g.new_vp("string") #attaches the URL to the vertices. This is useful for displaying the URL

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
def addNode(payload):
    load = json.loads(payload)
    #nodes: python dict {node:[children]}
    #if not already in map, create + add to map
    for nodes in load:
        node = nodes["url"]
        if node not in vert_map:
            #add to map
            n = g.add_vertex()
            vert_map[node] = n
            prop_vp[n] = node
        for child in nodes["child_nodes"]:
            #if child not in graph yet
            if child not in vert_map:
                n = g.add_vertex()
                vert_map[child] = n
                prop_vp[n] = child
                g.add_edge(vert_map[node], vert_map[child])
            else: #child already in graph
                g.add_edge(vert_map[node], vert_map[child])
    return 0

#removes specified node and all connecting edges
def removeNode(url):
    if url in vert_map:
        g.remove_vertex(vert_map[url])
        vert_map.pop(url)
        return 0 #success
    return -1 #failure
    
    
#testing and driver code. Will not be used in the final product.
if __name__ == '__main__':
    payload = '[{"url":"www.google.com","child_nodes":["www.abc.com","www.def.com"]},{"url":"www.rpi.edu","child_nodes":["www.google.com","www.abc.com"]}]'

    addNode(payload)
    graph_tool.draw.graph_draw(g, 
                    edge_pen_width=5,
                    vertex_text=prop_vp, 
                    vertex_aspect=1, 
                    vertex_text_position=1, 
                    vertex_text_color='black',
                    vertex_font_family='sans',
                    vertex_font_size=11,
                    vertex_color=None,
                    vertex_size=20,
                    output="mygraph.png"
                   )
    removeNode("www.abc.com")
    graph_tool.draw.graph_draw(g, 
                    edge_pen_width=5,
                    vertex_text=prop_vp, 
                    vertex_aspect=1, 
                    vertex_text_position=1, 
                    vertex_text_color='black',
                    vertex_font_family='sans',
                    vertex_font_size=11,
                    vertex_color=None,
                    vertex_size=20,
                    output="delgraph.png"
                   )
                   