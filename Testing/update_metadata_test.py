import graph_manip as gm
from pydantic import BaseModel
# Schema for Evaluation Team
class evaluation_payload(BaseModel):
	list_of_clicked_links: list
	click_count: list

"""
Tests:
- Empty webgraph
- Webgraph with nodes
- Webgraph with nodes and edges

- Node in graph
- Node not in graph
"""

def print_graph():
    print("  Vertices: ", end="")
    for v in gm.g.vertices():
        print(f"{gm.node_url[v]} {gm.click_count[v]}| ", end="")
    print()

def update_metadata_test(payload: evaluation_payload, expected_result):
    # print(payload.list_of_clicked_links)
    # print()
    print(f"update_metadata_node({payload}): expected = {expected_result}, actual = {gm.update_metadata(payload)}")
    print_graph()

print("Empty webgraph:")
print_graph()
update_metadata_test(evaluation_payload(
    list_of_clicked_links = ["www.google.com"], 
    click_count = [1]
), False)
update_metadata_test(evaluation_payload(
    list_of_clicked_links = ["www.rpi.edu"],
    click_count = [10] 
), False)

v = gm.g.add_vertex()
gm.node_url[v] = "www.hi.com"
gm.click_count[v] = 0
v = gm.g.add_vertex()
gm.node_url[v] = "www.google.com"
gm.click_count[v] = 100
v = gm.g.add_vertex()
gm.node_url[v] = "www.rpi.edu"
gm.click_count[v] = 10

print("\nWebgraph with only nodes:")
print_graph()
update_metadata_test(evaluation_payload(
     list_of_clicked_links = ["www.google.com"],
     click_count = [1]
), True)
update_metadata_test(evaluation_payload(
     list_of_clicked_links = ["www.google.com", "www.rpi.edu"],
     click_count = [10, 10]
), True)

gm.g.clear()
v = gm.g.add_vertex()
gm.node_url[v] = "www.hi.com"
gm.click_count[v] = 0
v = gm.g.add_vertex()
gm.node_url[v] = "www.google.com"
gm.click_count[v] = 100
v = gm.g.add_vertex()
gm.node_url[v] = "www.rpi.edu"
gm.click_count[v] = 10

print("Reset graph")
print_graph()
update_metadata_test(evaluation_payload(
     list_of_clicked_links = ["www.googly.com"],
     click_count = [1]
), True)
update_metadata_test(evaluation_payload(
     list_of_clicked_links = ["www.googy.com", "www.raspy.edu"],
     click_count = [10, 10]
), True)

gm.g.clear()
v = gm.g.add_vertex()
gm.node_url[v] = "www.hi.com"
gm.click_count[v] = 0
v = gm.g.add_vertex()
gm.node_url[v] = "www.google.com"
gm.click_count[v] = 100
v = gm.g.add_vertex()
gm.node_url[v] = "www.rpi.edu"
gm.click_count[v] = 10

print("\nWeird payloads:")
print_graph()
update_metadata_test(evaluation_payload(
     list_of_clicked_links = ["www.google.com", "www.rpi.edu"],
     click_count = [1,2,3]
), False)
update_metadata_test(evaluation_payload(
     list_of_clicked_links = ["www.google.com", "www.rpi.edu"],
     click_count = [1]
), False)
update_metadata_test(evaluation_payload(
     list_of_clicked_links = ["www.google.com", "www.rpi.edu"],
     click_count = []
), False)
update_metadata_test(evaluation_payload(
     list_of_clicked_links = [],
     click_count = [1,2,3]
), False)
update_metadata_test(evaluation_payload(
     list_of_clicked_links = [],
     click_count = []
), True)