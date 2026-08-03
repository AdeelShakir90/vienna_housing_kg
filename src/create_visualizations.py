from pathlib import Path
import pickle

import matplotlib.pyplot as plt
import pandas as pd


# Resolve paths relative to the project root so the script works from different
# working directories.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"
RESULTS_DIR = PROJECT_ROOT / "results"
FIGURES_DIR = RESULTS_DIR / "figures"
TABLES_DIR = RESULTS_DIR / "tables"

HOUSING_PRICES_FILE = DATA_RAW_DIR / "housing_prices.csv"
GRAPH_FILE = RESULTS_DIR / "vienna_housing_graph.gpickle"
SUMMARY_FILE = TABLES_DIR / "district_accessibility_summary.csv"


def load_graph():
    """Load the saved Knowledge Graph with all node and edge attributes."""
    with GRAPH_FILE.open("rb") as file:
        return pickle.load(file)


def count_stations_by_district(graph):
    """Count incoming LOCATED_IN relationships for every district node."""
    station_counts = {}

    for district_node, district_data in graph.nodes(data=True):
        if district_data.get("type") != "District":
            continue

        station_count = 0
        for source_node, _, edge_data in graph.in_edges(district_node, data=True):
            source_type = graph.nodes[source_node].get("type")
            relationship = edge_data.get("relationship")

            if source_type == "Station" and relationship == "LOCATED_IN":
                station_count += 1

        station_counts[district_data["label"]] = station_count

    return station_counts


def create_summary_table(housing_prices, station_counts):
    """Combine price and accessibility data into one district-level table."""
    summary = housing_prices.copy()
    summary["station_count"] = summary["district"].map(station_counts).fillna(0)
    summary["station_count"] = summary["station_count"].astype(int)

    # In this project, the accessibility score is defined as the number of
    # transport stations connected to a district.
    summary["accessibility_score"] = summary["station_count"]

    return summary[
        ["district", "avg_price_eur_m2", "station_count", "accessibility_score"]
    ]


def save_price_bar_chart(summary):
    """Create a bar chart showing average housing price by district."""
    chart_data = summary.sort_values("avg_price_eur_m2", ascending=False)

    plt.figure(figsize=(12, 7))
    plt.bar(chart_data["district"], chart_data["avg_price_eur_m2"], color="#4C78A8")
    plt.title("Average Housing Price by Vienna District")
    plt.xlabel("District")
    plt.ylabel("Average price (EUR per m2)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "district_prices_bar_chart.png", dpi=300)
    plt.close()


def save_accessibility_bar_chart(summary):
    """Create a bar chart showing station count by district."""
    chart_data = summary.sort_values("station_count", ascending=False)

    plt.figure(figsize=(12, 7))
    plt.bar(chart_data["district"], chart_data["station_count"], color="#F58518")
    plt.title("Accessibility Score by Vienna District")
    plt.xlabel("District")
    plt.ylabel("Number of transport stations")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "accessibility_score_bar_chart.png", dpi=300)
    plt.close()


def save_price_vs_accessibility_scatter(summary):
    """Create a scatter plot comparing price and accessibility score."""
    plt.figure(figsize=(10, 7))
    plt.scatter(
        summary["accessibility_score"],
        summary["avg_price_eur_m2"],
        color="#54A24B",
        s=90,
        alpha=0.85,
    )

    # Add readable district labels next to each point so the plot can be
    # interpreted without a separate legend.
    for _, row in summary.iterrows():
        plt.annotate(
            row["district"],
            (row["accessibility_score"], row["avg_price_eur_m2"]),
            textcoords="offset points",
            xytext=(6, 4),
            fontsize=8,
        )

    plt.title("Housing Price Compared with Accessibility")
    plt.xlabel("Accessibility score (number of transport stations)")
    plt.ylabel("Average price (EUR per m2)")
    plt.grid(True, linestyle="--", alpha=0.35)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "price_vs_accessibility_scatter.png", dpi=300)
    plt.close()


def main():
    # Load the housing price data and graph-based accessibility information.
    housing_prices = pd.read_csv(HOUSING_PRICES_FILE)
    graph = load_graph()
    station_counts = count_stations_by_district(graph)

    # Ensure output folders exist before writing tables and figures.
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    TABLES_DIR.mkdir(parents=True, exist_ok=True)

    # Create and save the combined district-level summary table.
    summary = create_summary_table(housing_prices, station_counts)
    summary.to_csv(SUMMARY_FILE, index=False)

    # Generate the requested visualization files.
    save_price_bar_chart(summary)
    save_accessibility_bar_chart(summary)
    save_price_vs_accessibility_scatter(summary)

    print("Visualizations and summary table created.")
    print(f"Saved: {FIGURES_DIR / 'district_prices_bar_chart.png'}")
    print(f"Saved: {FIGURES_DIR / 'accessibility_score_bar_chart.png'}")
    print(f"Saved: {FIGURES_DIR / 'price_vs_accessibility_scatter.png'}")
    print(f"Saved: {SUMMARY_FILE}")


if __name__ == "__main__":
    main()
