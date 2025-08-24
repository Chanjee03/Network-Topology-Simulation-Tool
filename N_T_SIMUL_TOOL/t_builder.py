from pygraphviz import AGraph
import networkx as nx
import matplotlib.pyplot as plt
import os
import sys

def build_graphviz_topology(links, output_file):
    try:
        dot = AGraph(comment="Network Topology", format="png")
        for a, b, label, color in links:
            dot.add_node(a, shape="box", color=color)
            dot.add_node(b, shape="box", color=color)
            dot.add_edge(a, b, label=label)

        # Try drawing with default 'dot' program
        try:
            dot.draw(output_file, prog="dot")
            print(f"Graphviz diagram saved as {output_file}.png")
        except OSError:
            # If 'dot' not found, provide guidance
            print("ERROR: Graphviz executable 'dot' not found.")
            print("Make sure Graphviz is installed and its 'bin' folder is in your PATH.")
            # Optional: try full path if known
            # dot_path = r"C:\Program Files\Graphviz\bin\dot.exe"
            # dot.draw(output_file, prog=dot_path)

    except Exception as e:
        print(f"Failed to build Graphviz topology: {e}")
        sys.exit(1)


def build_matplotlib_topology(links):
    G = nx.Graph()
    for a, b, label, _ in links:
        G.add_edge(a, b, label=label)

    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=2000, font_weight="bold")
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels={(a, b): label for a, b, label, _ in links}
    )
    plt.title("Network Topology - Interactive View")
    plt.show()
