from collections import defaultdict
from pathlib import Path
import pickle


# Resolve paths relative to the project root so the script can be run from
# different working directories.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
GRAPH_FILE = PROJECT_ROOT / "results" / "vienna_housing_graph.gpickle"
TABLES_DIR = PROJECT_ROOT / "results" / "tables"
INSIGHTS_FILE = TABLES_DIR / "project_insights.txt"


def load_graph():
    """Load the saved Knowledge Graph with its node and edge attributes."""
    with GRAPH_FILE.open("rb") as file:
        return pickle.load(file)


def count_station_edges(graph, district_node):
    """Count incoming LOCATED_IN edges from stations to one district."""
    station_count = 0

    # In the graph model, accessibility is based on Station --> District edges.
    for source_node, _, edge_data in graph.in_edges(district_node, data=True):
        source_type = graph.nodes[source_node].get("type")
        relationship = edge_data.get("relationship")

        if source_type == "Station" and relationship == "LOCATED_IN":
            station_count += 1

    return station_count


def build_district_summary(graph):
    """Create a district-level list with price and accessibility information."""
    district_summary = []

    for node, data in graph.nodes(data=True):
        if data.get("type") != "District":
            continue

        # The accessibility score is defined as the number of connected
        # transport stations for the district.
        accessibility_score = count_station_edges(graph, node)

        district_summary.append(
            {
                "district": data["label"],
                "avg_price_eur_m2": data["avg_price_eur_m2"],
                "accessibility_score": accessibility_score,
            }
        )

    return district_summary


def average_price_by_accessibility_score(district_summary):
    """Calculate average district price for each accessibility score."""
    prices_by_score = defaultdict(list)

    for row in district_summary:
        prices_by_score[row["accessibility_score"]].append(row["avg_price_eur_m2"])

    averages = {}
    for score, prices in prices_by_score.items():
        averages[score] = sum(prices) / len(prices)

    return dict(sorted(averages.items()))


def main():
    graph = load_graph()
    district_summary = build_district_summary(graph)

    # Insight 1 and 2 focus only on districts with accessibility score >= 3.
    highly_accessible_districts = [
        row for row in district_summary if row["accessibility_score"] >= 3
    ]

    most_expensive_high_access = max(
        highly_accessible_districts,
        key=lambda row: row["avg_price_eur_m2"],
    )
    cheapest_high_access = min(
        highly_accessible_districts,
        key=lambda row: row["avg_price_eur_m2"],
    )

    # Insight 3 groups prices by accessibility score.
    average_prices = average_price_by_accessibility_score(district_summary)

    insight_lines = []

    # Create short report-style sentences from the computed graph results.
    insight_lines.append(
        "The most expensive highly accessible district is "
        f"{most_expensive_high_access['district']} with an average price of "
        f"{most_expensive_high_access['avg_price_eur_m2']} EUR/m2 and an "
        f"accessibility score of {most_expensive_high_access['accessibility_score']}."
    )
    insight_lines.append(
        "The cheapest highly accessible district is "
        f"{cheapest_high_access['district']} with an average price of "
        f"{cheapest_high_access['avg_price_eur_m2']} EUR/m2 and an "
        f"accessibility score of {cheapest_high_access['accessibility_score']}."
    )

    for score, average_price in average_prices.items():
        insight_lines.append(
            "The average housing price for districts with accessibility score "
            f"{score} is {average_price:.2f} EUR/m2."
        )

    output_text = "\n".join(insight_lines)

    # Print the insights to the console for quick inspection.
    print(output_text)

    # Save the generated insights for the portfolio report.
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    INSIGHTS_FILE.write_text(output_text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
