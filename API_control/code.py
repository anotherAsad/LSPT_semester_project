#! /usr/bin/python3

from fastapi import FastAPI
from pydantic import BaseModel

import json
import graph_manip
import time
import threading

import asyncio
import uvicorn

import random

app = FastAPI()

pagerank_call_count = 0

######################################## UI/UX INTERFACE ########################################
@app.get("/uiux/graph")
async def return_graph():
	graph_manip.graph_update_mutex.acquire()		# acquire mutex lock
	json_graph = graph_manip.convert_graph_to_JSON(graph_manip.g)
	graph_manip.graph_update_mutex.release()		# release mutex lock
	
	return json_graph

# TODO: implement sub graphing
@app.get("/uiux/subgraph/{url}/{depth}")
async def return_subgraph(url:str, depth:int):
	graph_manip.graph_update_mutex.acquire()		# acquire mutex lock
	
	# create a subgraph.
	subg, urls, rank, click_count = graph_manip.get_subgraph(url, depth)

	# return None if the URL was not found
	if subg == None:
		json_graph = {}
	else:
		json_graph = graph_manip.convert_subgraph_to_JSON(subg, urls, rank, click_count)

	graph_manip.graph_update_mutex.release()		# release mutex lock	
	return json_graph

####################################### RANKING INTERFACE #######################################
@app.get("/ranking/{url}")
async def return_score(url:str):
	graph_manip.graph_update_mutex.acquire()		# acquire mutex lock

	node = graph_manip.find_in_graph(url)
	return_json = {"pageRank": None, "inLinkCount": None, "outLinkCount": None}

	if (node is not None) and (graph_manip.page_rank is not None):
		return_json["pageRank"] = graph_manip.page_rank[node]
		return_json["inLinkCount"] = int(graph_manip.g.get_in_degrees([node])[0])
		return_json["outLinkCount"] = int(graph_manip.g.get_out_degrees([node])[0])
		print(return_json)

	graph_manip.graph_update_mutex.release()		# release mutex lock

	return return_json
###################################### CRAWLING INTERFACE #######################################
class crawling_payload(BaseModel):
	url: str
	child_nodes: list

@app.post("/crawling/add_nodes")
async def update_link_graph(add_node_payload: crawling_payload):
	graph_manip.graph_update_mutex.acquire()		# acquire mutex lock
	# call the wrapped function
	graph_manip.add_nodes(add_node_payload.json())
	graph_manip.graph_update_mutex.release()		# release mutex lock

	return {"nodes_added": True}

@app.get("/crawling/remove_node/{url}")
async def remove_node(url:str):
	graph_manip.graph_update_mutex.acquire()		# acquire mutex lock
	result = graph_manip.remove_node(url)
	graph_manip.graph_update_mutex.release()		# release mutex lock

	return {"node_removed": result}

##################################### EVALUATION INTERFACE ######################################
# Schema for Evaluation Team
class evaluation_payload(BaseModel):
	list_of_clicked_links: list
	click_count: list

@app.post("/evaluation/update_metadata")
async def update_metadata(add_eval_payload: evaluation_payload):
	graph_manip.graph_update_mutex.acquire()		# acquire mutex lock
	return_code = graph_manip.update_metadata(add_eval_payload)
	graph_manip.graph_update_mutex.release()		# release mutex lock

	return return_code

# Report metric is called by US.

##################################### LINK ANALYSIS INTERFACE ######################################
@app.get("/run_pagerank")
async def run_pagerank():
	update_pagerank()
	return True

@app.get("/visualize_graph")
async def visualize_graph():
	graph_manip.visualize_graph("new_graph.png")

	return True

@app.get("/print_scores")
async def print_scores():
	graph_manip.graph_update_mutex.acquire()		# acquire mutex lock

	if graph_manip.page_rank is not None:
		print("\nPageRank scores:")
		for v in graph_manip.g.vertices():
			print(f"{graph_manip.node_url[v]}: {graph_manip.page_rank[v]}")

	graph_manip.graph_update_mutex.release()		# release mutex lock

	return True

@app.get("/print_stats")
async def print_stats():
	global pagerank_call_count
	print(f"pagerank_call_count: {pagerank_call_count}")

	return True

# Report metric is called by US.
#################################################################################################

# Updates page rank
def update_pagerank():
	global pagerank_call_count

	# Do not run page_rank if the graph is empty
	if graph_manip.g.num_vertices() == 0:
		return False

	# acquire mutex
	graph_manip.graph_update_mutex.acquire()

	pagerank_call_count += 1
	print(f"[PageRank Call: {pagerank_call_count}]")

	graph_manip.page_rank = graph_manip.pagerank(graph_manip.g)

	# release mutex
	graph_manip.graph_update_mutex.release()

	return True

################################################################################################################
#testing and driver code. Will ~not~ be used in the final product.

if True:
	payload = '[{"url":"www.google.com","child_nodes":["www.abc.com","www.def.com"]},{"url":"www.rpi.edu","child_nodes":["www.google.com","www.abc.com"]}]'

	graph_manip.add_nodes(payload)

	graph_manip.add_nodes('{"url":"www.boogle.com"}')

	update_pagerank()

	graph_manip.visualize_graph("mygraph.png")

	graph_manip.remove_node("www.abc.com")

	update_pagerank()

	graph_manip.visualize_graph("delgraph.png")

	if graph_manip.page_rank is not None:
		print("\nPageRank scores:")
		for v in graph_manip.g.vertices():
			print(f"{graph_manip.node_url[v]}: {graph_manip.page_rank[v]}")
				
print("Doing Good. Will spawn timed_processing_loop and run_server")


################################################################################################################
# Main Routine
shutdown = False

# DESCRIPTION: Calls pagerand and Performs JSON dumps of graph after set interval.
async def timed_processing_loop():
	# BOOTUP SECTION
	# TODO: Read from the stored json

	get_graph_as_json = lambda: graph_manip.convert_graph_to_JSON(graph_manip.g)

	# RUNNING SECTION
	while not shutdown:
		update_pagerank()
		await asyncio.sleep(10)

		# After every 15 minutes save the graph
		if pagerank_call_count > 1 and pagerank_call_count % 10 == 0:
			with open("graph.json", "w") as file:
				json.dump(get_graph_as_json(), file, indent=4)

	# SHUTDOWN SECTION: whenever the system shuts down, we save the graph downstream 
	with open("graph.json", "w") as file:
		json.dump(get_graph_as_json(), file, indent=4)

	print("JSON dump of graph complete!\nClosing timed_processing_loop.")
	return

# DESCRIPTION: Spawns an HTTP server that is used for interfacing with components of other teams.
async def run_server():
	global shutdown

	config = uvicorn.Config("code:app", port=1234, log_level="info", host="lspt-link-analysis.cs.rpi.edu", reload=True)
	server = uvicorn.Server(config)
	await server.serve()

	shutdown = True

	print("Server shutdown complete.")
	return

# Main routine
async def main():
    server_task = asyncio.create_task(run_server())
    action_task = asyncio.create_task(timed_processing_loop())
    await asyncio.gather(server_task, action_task)

if __name__ == "__main__":
    asyncio.run(main())