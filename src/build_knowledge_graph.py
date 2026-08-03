from pathlib import Path
import pickle

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd


# Resolve paths relative to the project root so the script can be run from
# different working directories.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"
RESULTS_DIR = PROJECT_ROOT / "results"
FIGURES_DIR = RESULTS_DIR / "figures"

HOUSING_PRICES_FILE = DATA_RAW_DIR / "housing_prices.csv"
TRANSPORT_STATIONS_FILE = DATA_RAW_DIR / "transport_stations.csv"
GRAPH_FILE = RESULTS_DIR / "vienna_housing_graph.gpickle"
FIGURE_FILE = FIGURES_DIR / "knowledge_graph.png"


def main():
    # Load the source datasets with pandas.
    housing_prices = pd.read_csv(HOUSING_PRICES_FILE)
    transport_stations = pd.read_csv(TRANSPORT_STATIONS_FILE)

    # A directed graph is used because stations point to the districts where
    # they are located: Station --> District.
    graph = nx.DiGraph()

    # Create one node for each district and store the average price as an
    # attribute on the district node.
    for _, row in housing_prices.iterrows():
        district_name = row["district"]
        district_id = f"district:{district_name}"

        graph.add_node(
            district_id,
            label=district_name,
            type="District",
            avg_price_eur_m2=int(row["avg_price_eur_m2"]),
        )

    # Create station nodes and connect each station to the district where it is
    # located. Internal IDs avoid name collisions between stations and districts.
    for _, row in transport_stations.iterrows():
        station_name = row["station"]
        district_name = row["district"]
        station_id = f"station:{station_name}"
        district_id = f"district:{district_name}"

        graph.add_node(
            station_id,
            label=station_name,
            type="Station",
            transport_type=row["transport_type"],
        )
        graph.add_edge(
            station_id,
            district_id,
            relationship="LOCATED_IN",
        )

    # Make sure the output folders exist before saving generated files.
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    # Save the graph in gpickle format. This keeps all node and edge attributes.
    with GRAPH_FILE.open("wb") as file:
        pickle.dump(graph, file, protocol=pickle.HIGHEST_PROTOCOL)

    # Draw a simple visual overview of the Knowledge Graph using different
    # colors for district and station nodes.
    node_colors = [
        "#4C78A8" if data["type"] == "District" else "#F58518"
        for _, data in graph.nodes(data=True)
    ]
    labels = {node: data["label"] for node, data in graph.nodes(data=True)}

    plt.figure(figsize=(14, 10))
    positions = nx.spring_layout(graph, seed=42, k=0.55)
    nx.draw_networkx_nodes(
        graph,
        positions,
        node_color=node_colors,
        node_size=900,
        alpha=0.95,
    )
    nx.draw_networkx_edges(
        graph,
        positions,
        arrows=True,
        arrowstyle="-|>",
        arrowsize=14,
        edge_color="#666666",
        alpha=0.65,
    )
    nx.draw_networkx_labels(
        graph,
        positions,
        labels=labels,
        font_size=8,
        font_family="sans-serif",
    )

    # Add a compact legend so the colors are easy to interpret.
    district_marker = plt.Line2D(
        [0],
        [0],
        marker="o",
        color="w",
        markerfacecolor="#4C78A8",
        markersize=10,
        label="District",
    )
    station_marker = plt.Line2D(
        [0],
        [0],
        marker="o",
        color="w",
        markerfacecolor="#F58518",
        markersize=10,
        label="Station",
    )
    plt.legend(handles=[district_marker, station_marker], loc="best")
    plt.title("Vienna Housing and Accessibility Knowledge Graph")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(FIGURE_FILE, dpi=300)
    plt.close()

    # Print summary statistics for quick inspection after running the script.
    number_of_districts = sum(
        1 for _, data in graph.nodes(data=True) if data["type"] == "District"
    )
    number_of_stations = sum(
        1 for _, data in graph.nodes(data=True) if data["type"] == "Station"
    )

    print("Knowledge Graph Summary")
    print("-----------------------")
    print(f"Number of nodes: {graph.number_of_nodes()}")
    print(f"Number of edges: {graph.number_of_edges()}")
    print(f"Number of districts: {number_of_districts}")
    print(f"Number of stations: {number_of_stations}")
    print(f"Graph saved to: {GRAPH_FILE}")
    print(f"Visualization saved to: {FIGURE_FILE}")


if __name__ == "__main__":
    main()
