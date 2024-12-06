#! /usr/bin/python3

from fastapi import FastAPI
from pydantic import BaseModel

import json
import graph_manip

app = FastAPI()

######################################## UI/UX INTERFACE ########################################
def get_graph_as_json():
	return {"base_node": []}

@app.get("/uiux/graph")
async def return_graph():
	return get_graph_as_json()

@app.get("/uiux/subgraph")
async def return_subgraph():
	return get_graph_as_json().base_node

####################################### RANKING INTERFACE #######################################
def get_score(url):
	return 0.0

@app.get("/ranking/score/{url}")
async def return_score(url):
	return get_score(url)

###################################### CRAWLING INTERFACE #######################################

# Node Payload schema
class node_payload:
	url: str
	child_nodes: list

@app.post("/crawling/add_nodes")
async def update_link_graph(node_payload):
	# TODO: Write code here to pass the schema on
	return True

@app.get("/crawling/remove_node/{url}")
async def remove_node(url):
	return True

##################################### EVALUATION INTERFACE ######################################
# Schema for Evaluation Team
class evaluation_payload(BaseModel):
	url: str
	clicks: float
	time: float

@app.post("/evaluation/update_metadata")
async def update_metadata(evaluation_payload):
	# TODO: Write code here to pass the schema on
	return True

# Report metric is called by US.
#################################################################################################


#testing and driver code. Will ~not~ be used in the final product.
payload = '[{"url":"www.google.com","child_nodes":["www.abc.com","www.def.com"]},{"url":"www.rpi.edu","child_nodes":["www.google.com","www.abc.com"]}]'

graph_manip.add_node(payload)

graph_manip.graph_tool.draw.graph_draw(
				graph_manip.g, 
				edge_pen_width=5,
				vertex_text=graph_manip.node_url, 
				vertex_aspect=1, 
				vertex_text_position=1, 
				vertex_text_color='black',
				vertex_font_family='sans',
				vertex_font_size=11,
				vertex_color=None,
				vertex_size=20,
				output="mygraph.png"
				)

graph_manip.remove_node("www.abc.com")

graph_manip.graph_tool.draw.graph_draw(
				graph_manip.g, 
				edge_pen_width=5,
				vertex_text=graph_manip.node_url, 
				vertex_aspect=1, 
				vertex_text_position=1, 
				vertex_text_color='black',
				vertex_font_family='sans',
				vertex_font_size=11,
				vertex_color=None,
				vertex_size=20,
				output="delgraph.png"
)

pr = graph_manip.pagerank(graph_manip.g)

print("\nPageRank scores:")
for v in graph_manip.g.vertices():
    print(f"{graph_manip.node_url[v]}: {pr[v]}")
				
print("Doing good")