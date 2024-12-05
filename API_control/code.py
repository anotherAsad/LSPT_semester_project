#! /usr/bin/python3

from fastapi import FastAPI
from pydantic import BaseModel

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
async def receive_node_payload(node_payload):
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

@app.post("/evaluation/update_link_graph")
async def update_link_graph(evaluation_payload):
	# TODO: Write code here to pass the schema on
	return True

# Report metric is called by US.
#################################################################################################

@app.get("/")
async def root():
	return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
	return {"item_id": item_id, "q": q}

# Schemas
class Item(BaseModel):
	name: str
	description: str = None
	price: float
	tax: float = None

@app.post("/items/")
async def create_item(item: Item):
	print("Item posted")
	print(f"{item.name}, {item.description}, {item.price}")
	return item
	