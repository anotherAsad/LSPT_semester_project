#! /usr/bin/python3

from fastapi import FastAPI
from pydantic import BaseModel

import json
import graph_manip

app = FastAPI()

######################################## UI/UX INTERFACE ########################################
def get_graph_as_json():
	json_graph = graph_manip.convert_graph_to_JSON(graph_manip.g)
	return json_graph

@app.get("/uiux/graph")
async def return_graph():
	return get_graph_as_json()

# TODO: implement sub graphing
@app.get("/uiux/subgraph/{url}")
async def return_subgraph(url):
	return get_graph_as_json()

####################################### RANKING INTERFACE #######################################
@app.get("/ranking/{url}")
async def return_score(url):
	node = graph_manip.find_in_graph(url)
	return_json = {"pageRank": None, "inLinkCount": None, "outLinkCount": None}

	if (node is not None) and (graph_manip.page_rank is not None):
		return_json["pageRank"] = graph_manip.page_rank[node]
		return_json["inLinkCount"] = int(graph_manip.g.get_in_degrees([node])[0])
		return_json["outLinkCount"] = int(graph_manip.g.get_out_degrees([node])[0])
		print(return_json)

	return return_json
###################################### CRAWLING INTERFACE #######################################
@app.post("/crawling/add_nodes")
async def update_link_graph(node_payload):
	print(node_payload)
	# TODO: Write code here to pass the schema on
	return True

@app.get("/crawling/remove_node/{url}")
async def remove_node(url):
	return {"node_removed": graph_manip.remove_node(url)}

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

# Updates page rank
def update_pagerank():
	# acquire mutex
	graph_manip.update_mutex.acquire()

	graph_manip.page_rank = graph_manip.pagerank(graph_manip.g)

	# update the text that is to be shown in graph visualization
	for node in graph_manip.g.vertices():
		graph_manip.node_text[node] = f"{graph_manip.node_url[node]}: {graph_manip.page_rank[node]:.3f}"

	# release mutex
	graph_manip.update_mutex.release()

	return

#################################################################################################
#testing and driver code. Will ~not~ be used in the final product.
payload = '[{"url":"www.google.com","child_nodes":["www.abc.com","www.def.com"]},{"url":"www.rpi.edu","child_nodes":["www.google.com","www.abc.com"]}]'

graph_manip.add_node(payload)

graph_manip.add_node('{"url":"www.boogle.com"}')

update_pagerank()

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

graph_manip.remove_node("www.abc.com")

update_pagerank()

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
	output="delgraph.png"
)

if graph_manip.page_rank is not None:
	print("\nPageRank scores:")
	for v in graph_manip.g.vertices():
		print(f"{graph_manip.node_url[v]}: {graph_manip.page_rank[v]}, {graph_manip.g.get_in_degrees([v])[0]}")


				
print("Doing good")