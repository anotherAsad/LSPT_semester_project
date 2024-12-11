import graph_manip 

# Test 1: Add new url and new list_of_outlinks.
# Preconditions: The webgraph is instantiated. Has no nodes.
# Returns: success (0)
print("returned: " + str(graph_manip.add_nodes(
"""
{
    "url": "www.google.com", 
    "child_nodes": [
        "www.wikipedia.com",
        "www.cnn.com"
    ]
}
"""
)))

graph_manip.page_rank = graph_manip.pagerank(graph_manip.g)
graph_manip.visualize_graph("graph1.png")

# Test 2: Add a url that is already in the graph, with new outlinks
# Preconditions: The webgraph is instantiated, has node with url
# “www.google.com”, but doesn’t have “www.rpi.edu”, “www.rpi.com”
# Returns: success
print("returned: " + str(graph_manip.add_nodes(
"""
{
    "url": "www.google.com", 
    "child_nodes": [
        "www.wikipedia.com",
        "www.rpi.edu"
    ]
}
"""
)))

graph_manip.page_rank = graph_manip.pagerank(graph_manip.g)
graph_manip.visualize_graph("graph2.png")

"""
# Test 3: Add a url that is not in the graph, but has outlinks that are
# in the graph.
# Preconditions: The webgraph is instantiated, does not have node with
# url “www.boogle.com”, but has “www.rpi.edu”, “www.rpi.com”
# Returns: success
print("returned: " + str(add_node("www.boogle.com", [
“www.rpi.edu”,
“www.rpi.com”
]))
# Test 4: Add a url that is in the graph, with outlinks that are already
# in the graph.
# Preconditions: The webgraph is instantiated, has nodes with
# urls “www.boogle.com”
# Returns: success
print("returned: " + str(add_node("www.boogle.com", [
“www.rpi.edu”,
“www.rpi.com”
]))
# Test 5: Add a url that is in the graph, with a mix of outlinks; (some new, #
some old)
# Preconditions: The webgraph is instantiated, has nodes with
# urls “www.boogle.com”, “www.rpi.edu”. Doesn’t have “www.cnn.com”
# Returns: success
print("returned: " + str(add_node("www.boogle.com", [
“www.rpi.edu”,
“www.rpi.com”,
“www.cnn.com”
]))
# Test 6: Test with non-string argument for url, but valid list_of_outlinks
# Preconditions: The webgraph is instantiated.
# Returns: failure
print("returned: " + str(add_node(1234, [
“www.rpi.edu”,
“www.rpi.com”,
“www.cnn.com”
]))
# Test 7: Test with valid string url, and non-list argument for
# list_of_outlinks
# Preconditions: The webgraph is instantiated.
# Returns: failure
print("returned: " + str(add_node("www.boogle.com", 1234))
# Test 8: Test with not-string and non-list argument for url and
# list_of_outlinks respectively
# Preconditions: The webgraph is instantiated.
# Returns: failure
print("returned: " + str(add_node([], 1234))
# Test 9: Test with valid url, and empty list_of_strings
# Preconditions: The webgraph is instantiated.
# Returns: success
print("returned: " + str(add_node("www.boogle.com", []))
# Test 10: Test with valid url, and a list_of_outlinks, some of whose
# arguments are not strings.
# Preconditions: The webgraph is instantiated.
# Returns: failure
print("returned: " + str(add_node("www.boogle.com", [
“www.cnn.com”
1234
]))
"""