import graph_manip 
import random
import json

def scalibility_test(node_count):
	global shutdown
	characters = "abcdefghijklmnopqrstuvwxyz"  # Includes a-z, A-Z, and 0-9
	url_list = []

	generate_random_string = lambda length: ''.join(random.choices(characters, k=length))

	while len(url_list) < node_count:
		url = generate_random_string(random.randint(5, 15))
		url_list.append(url)

		random_picks = random.sample(url_list, min(random.randint(1, 10), len(url_list)))

		arg = {
			"url": url,
			"child_nodes": random_picks
		}

		json_string = json.dumps(arg)

		graph_manip.add_nodes(json_string)

	print(f"{node_count} nodes added successfully. Running page rank...")

	graph_manip.page_rank = graph_manip.pagerank(graph_manip.g)

	print("Page Rank Done...")

	print(f"Graph has {graph_manip.g.num_vertices()} nodes and {graph_manip.g.num_edges()} edges\n")


	check_list = random.sample(url_list, 16)

	for url in check_list:
		print(f"www.{url}.com, page_rank: {graph_manip.page_rank[graph_manip.find_in_graph(url)]}")

	return

def test_add_nodes():
	# Test 1: Add new url and new list_of_outlinks.
	# Preconditions: The webgraph is instantiated. Has no nodes.
	# Returns: success (0)
	print("Test 1 returned: " + str(graph_manip.add_nodes(
	"""
	{
		"url": "www.google.com", 
		"child_nodes": [
			"www.wikipedia.com",
			"www.cnn.com"
		]
	}
	"""
	)), )

	# Test 2: Add a url that is already in the graph, with new outlinks
	# Preconditions: The webgraph is instantiated, has node with url
	# "www.google.com", but doesn’t have "www.rpi.edu", "www.rpi.com"
	# Returns: success
	print("Test 2 returned: " + str(graph_manip.add_nodes(
	"""
	{
		"url": "www.google.com", 
		"child_nodes": [
			"www.wikipedia.com",
			"www.rpi.edu"
		]
	}
	"""
	)), f"expected {0}")

	# Test 3: Add a url that is not in the graph, but has outlinks that are
	# in the graph.
	# Preconditions: The webgraph is instantiated, does not have node with
	# url "www.boogle.com", but has "www.rpi.edu", "www.rpi.com"
	# Returns: success
	print("Test 3 returned: " + str(graph_manip.add_nodes(
	"""
	{
		"url": "www.boogle.com",
		"child_nodes": [
			"www.rpi.edu",
			"www.rpi.com"
		]
	}
	"""
	)), f"expected {0}")

	# Test 4: Add a url that is in the graph, with outlinks that are already
	# in the graph.
	# Preconditions: The webgraph is instantiated, has nodes with
	# urls "www.boogle.com"
	# Returns: success
	print("Test 4 returned: " + str(graph_manip.add_nodes(
	"""
	{
		"url": "www.boogle.com",
		"child_nodes": [
			"www.rpi.edu",
			"www.rpi.com"
		]
	}
	"""
	)), f"expected {0}")

	# Test 5: Add a url that is in the graph, with a mix of outlinks; (some new, some old)
	# Preconditions: The webgraph is instantiated, has nodes with
	# urls "www.boogle.com", "www.rpi.edu". Doesn't have "www.cnn.com"
	# Returns: success
	print("Test 5 returned: " + str(graph_manip.add_nodes(
	"""
	{
		"url": "www.boogle.com",
		"child_nodes": [
			"www.rpi.edu",
			"www.rpi.com",
			"www.cnn.com"
		]
	}
	"""
	)), f"expected {0}")

	# Test 6: Test with non-string argument for url, but valid list_of_outlinks
	# Preconditions: The webgraph is instantiated.
	# Returns: failure
	print("Test 6 returned: " + str(graph_manip.add_nodes(
	"""
	{
		"url": 1234,
		"child_nodes": [
			"www.rpi.edu",
			"www.rpi.com",
			"www.cnn.com"
		]
	}
	"""
	)), f"expected {-1}")

	# Test 7: Test with valid string url, and non-list argument for
	# list_of_outlinks
	# Preconditions: The webgraph is instantiated.
	# Returns: failure
	print("Test 7 returned: " + str(graph_manip.add_nodes(
	"""
	{
		"url": "www.boogle.com",
		"child_nodes": 1234
	}
	"""
	)), f"expected {-1}")

	# Test 8: Test with not-string and non-list argument for url and
	# list_of_outlinks respectively
	# Preconditions: The webgraph is instantiated.
	# Returns: failure
	print("Test 8 returned: " + str(graph_manip.add_nodes(
	"""
	{
		"url": [],
		"child_nodes": 1234
	}
	"""
	)), f"expected {-1}")

	# Test 9: Test with valid url, and empty list_of_strings
	# Preconditions: The webgraph is instantiated.
	# Returns: success
	print("Test 9 returned: " + str(graph_manip.add_nodes(
	"""
	{
		"url": "www.boogle.com",
		"child_nodes": []
	}
	"""
	)), f"expected {0}")

	# Test 10: Test with valid url, and empty list_of_strings
	# Preconditions: The webgraph is instantiated.
	# Returns: success
	print("Test 10 returned: " + str(graph_manip.add_nodes(
	"""
	{
		"url": "www.boogle.com",
		"child_nodes": [
			"www.cnn.com",
			1234
		]
	}
	"""
	)), f"expected {0}")
	
	return

test_add_nodes()

scalibility_test(10000)