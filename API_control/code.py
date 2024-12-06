#! /usr/bin/python3

from fastapi import FastAPI
from pydantic import BaseModel

import json
import graph_manip
import time
import threading

import asyncio
import uvicorn

app = FastAPI()

pagerank_call_count = 0

######################################## UI/UX INTERFACE ########################################
def get_graph_as_json():
	json_graph = graph_manip.convert_graph_to_JSON(graph_manip.g)
	return json_graph

@app.get("/uiux/graph")
async def return_graph():
	graph_manip.update_mutex.acquire()		# acquire mutex lock
	ret_val = get_graph_as_json()
	graph_manip.update_mutex.release()		# release mutex lock
	
	return ret_val

# TODO: implement sub graphing
@app.get("/uiux/subgraph/{url}")
async def return_subgraph(url):
	graph_manip.update_mutex.acquire()		# acquire mutex lock
	ret_val = get_graph_as_json()
	graph_manip.update_mutex.release()		# release mutex lock
	
	return ret_val

####################################### RANKING INTERFACE #######################################
@app.get("/ranking/{url}")
async def return_score(url):
	graph_manip.update_mutex.acquire()		# acquire mutex lock

	node = graph_manip.find_in_graph(url)
	return_json = {"pageRank": None, "inLinkCount": None, "outLinkCount": None}

	if (node is not None) and (graph_manip.page_rank is not None):
		return_json["pageRank"] = graph_manip.page_rank[node]
		return_json["inLinkCount"] = int(graph_manip.g.get_in_degrees([node])[0])
		return_json["outLinkCount"] = int(graph_manip.g.get_out_degrees([node])[0])
		print(return_json)

	graph_manip.update_mutex.release()		# release mutex lock

	return return_json
###################################### CRAWLING INTERFACE #######################################
class crawling_payload(BaseModel):
	url: str
	child_nodes: list

@app.post("/crawling/add_nodes")
async def update_link_graph(add_node_payload: crawling_payload):
	graph_manip.update_mutex.acquire()		# acquire mutex lock
	# call the wrapped function
	graph_manip.add_node(add_node_payload.json())
	graph_manip.update_mutex.release()		# release mutex lock

	return {"nodes_added": True}

@app.get("/crawling/remove_node/{url}")
async def remove_node(url):
	graph_manip.update_mutex.acquire()		# acquire mutex lock
	result = graph_manip.remove_node(url)
	graph_manip.update_mutex.release()		# release mutex lock

	return {"node_removed": result}

##################################### EVALUATION INTERFACE ######################################
# Schema for Evaluation Team
class evaluation_payload(BaseModel):
	list_of_clicked_links: list
	click_count: list

@app.post("/evaluation/update_metadata")
async def update_metadata(evaluation_payload):
	graph_manip.update_mutex.acquire()		# acquire mutex lock
	graph_manip.update_metadata(evaluation_payload.json())
	graph_manip.update_mutex.release()		# release mutex lock

	return True

# Report metric is called by US.

##################################### LINK ANALYSIS INTERFACE ######################################
@app.get("/run_pagerank")
async def run_pagerank():
	update_pagerank()
	return True

@app.get("/visualize_graph")
async def visualize_graph():
	graph_manip.update_mutex.acquire()		# acquire mutex lock

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
		output="new_graph.png"
	)

	graph_manip.update_mutex.release()		# release mutex lock

	return True

@app.get("/print_scores")
async def print_scores():
	graph_manip.update_mutex.acquire()		# acquire mutex lock

	if graph_manip.page_rank is not None:
		print("\nPageRank scores:")
		for v in graph_manip.g.vertices():
			print(f"{graph_manip.node_url[v]}: {graph_manip.page_rank[v]}")

	graph_manip.update_mutex.release()		# release mutex lock

	return True

@app.get("/print_stats")
async def print_scores():
	print(f"pagerank_call_count: {pagerank_call_count}")

	return True

# Report metric is called by US.
#################################################################################################

# Updates page rank
def update_pagerank():
	global pagerank_call_count
	# acquire mutex
	graph_manip.update_mutex.acquire()

	pagerank_call_count += 1
	print(f"[PageRank Call: {pagerank_call_count}]")

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
		print(f"{graph_manip.node_url[v]}: {graph_manip.page_rank[v]}")


				
print("Doing Good. Will start pagerank thread")


################################################################################################################
# Main Routine
shutdown = False

async def pagerank_routine():
	while not shutdown:
		update_pagerank()
		await asyncio.sleep(10)

async def run_server():
	global shutdown
	
	config = uvicorn.Config("code:app", port=1234, log_level="info", host="lspt-link-analysis.cs.rpi.edu", reload=True)
	server = uvicorn.Server(config)
	await server.serve()

	shutdown = True

async def main():
    server_task = asyncio.create_task(run_server())
    action_task = asyncio.create_task(pagerank_routine())
    await asyncio.gather(server_task, action_task)

if __name__ == "__main__":
    asyncio.run(main())