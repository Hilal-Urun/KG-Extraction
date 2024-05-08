import json

import networkx as nx
from matplotlib import pyplot as plt
from parser import CodeAnalyzer


def _G_json_file(G):
    graph_data = {
        "nodes": list(G.nodes),
        "edges": list(G.edges)
    }

    graph_json = json.dumps(graph_data, indent=4)
    with open('graph.json', 'w') as f:
        f.write(graph_json)

    return


if __name__ == '__main__':
    directory_analyzer = CodeAnalyzer('/directory/to/analyze')
    directory_analyzer.analyze_directory()
    G = nx.DiGraph()

    "-------Directed Acyclic Graph ------"

    for node in directory_analyzer.graph['nodes']:
        G.add_node(node)

    for edge in directory_analyzer.graph['edges']:
        G.add_edge(*edge)

    try:
        cycle = nx.find_cycle(G, orientation='original')
        print(f"Cycle detected: {cycle}")
        G.remove_edge(cycle[0][0], cycle[0][1])
        print("An edge in the cycle was removed to make the graph acyclic.")
    except nx.NetworkXNoCycle:
        print("No cycle found, the graph is a DAG.")

    pos = nx.spring_layout(G)
    plt.figure(figsize=(50, 50))
    nx.draw(G, pos, with_labels=True, node_size=1500, node_color="lightblue", font_size=10, font_weight="bold")
    plt.savefig("dag.png")
    #for saving graph as json file
    #_G_json_file(G)
