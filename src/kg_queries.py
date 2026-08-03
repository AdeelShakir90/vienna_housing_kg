from pathlib import Path
import pickle


# Resolve project paths relative to this script so it can be run from the
# project root or from another working directory.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
GRAPH_FILE = PROJECT_ROOT / "results" / "vienna_housing_graph.gpickle"
TABLES_DIR = PROJECT_ROOT / "results" / "tables"
RESULTS_FILE = TABLES_DIR / "query_results.txt"


def get_district_nodes(graph):
    """Return district nodes with their graph attributes."""
    return [
        (node, data)
        for node, data in graph.nodes(data=True)
        if data.get("type") == "District"
    ]


def count_located_in_stations(graph, district_node):
    """Count stations connected to a district through LOCATED_IN edges."""
    station_count = 0

    # In this graph, LOCATED_IN edges point from Station --> District.
    for source_node, _, edge_data in graph.in_edges(district_node, data=True):
        source_type = graph.nodes[source_node].get("type")
        relationship = edge_data.get("relationship")

        if source_type == "Station" and relationship == "LOCATED_IN":
            station_count += 1

    return station_count


def format_table(headers, rows):
    """Create a simple plain-text table for console and file output."""
    all_rows = [headers] + rows
    column_widths = [
        max(len(str(row[column_index])) for row in all_rows)
        for column_index in range(len(headers))
    ]

    lines = []
    for row_index, row in enumerate(all_rows):
        line = " | ".join(
            str(value).ljust(column_widths[column_index])
            for column_index, value in enumerate(row)
        )
        lines.append(line)

        if row_index == 0:
            separator = "-+-".join("-" * width for width in column_widths)
            lines.append(separator)

    return "\n".join(lines)


def main():
    # Load the saved Knowledge Graph, including all node and edge attributes.
    with GRAPH_FILE.open("rb") as file:
        graph = pickle.load(file)

    district_nodes = get_district_nodes(graph)

    # Query 1: rank districts from highest to lowest average price.
    most_expensive = sorted(
        district_nodes,
        key=lambda item: item[1]["avg_price_eur_m2"],
        reverse=True,
    )[:5]

    # Query 2: rank districts from lowest to highest average price.
    cheapest = sorted(
        district_nodes,
        key=lambda item: item[1]["avg_price_eur_m2"],
    )[:5]

    # Query 3 and 4: count incoming LOCATED_IN relationships for each district.
    # This count is used as a simple accessibility score.
    accessibility_rows = []
    for district_node, data in district_nodes:
        number_of_stations = count_located_in_stations(graph, district_node)
        accessibility_rows.append(
            {
                "district": data["label"],
                "avg_price_eur_m2": data["avg_price_eur_m2"],
                "number_of_stations": number_of_stations,
                "accessibility_score": number_of_stations,
            }
        )

    districts_by_station_count = sorted(
        accessibility_rows,
        key=lambda row: row["number_of_stations"],
        reverse=True,
    )

    accessibility_ranked = sorted(
        accessibility_rows,
        key=lambda row: row["accessibility_score"],
        reverse=True,
    )

    # Query 5: identify the district with the highest accessibility score.
    most_accessible = accessibility_ranked[0]

    output_sections = []

    output_sections.append("Top 5 Most Expensive Districts")
    output_sections.append(
        format_table(
            ["Rank", "District", "Avg Price EUR/m2"],
            [
                [rank, data["label"], data["avg_price_eur_m2"]]
                for rank, (_, data) in enumerate(most_expensive, start=1)
            ],
        )
    )

    output_sections.append("\nTop 5 Cheapest Districts")
    output_sections.append(
        format_table(
            ["Rank", "District", "Avg Price EUR/m2"],
            [
                [rank, data["label"], data["avg_price_eur_m2"]]
                for rank, (_, data) in enumerate(cheapest, start=1)
            ],
        )
    )

    output_sections.append("\nDistricts With the Most Transport Stations")
    output_sections.append(
        format_table(
            ["Rank", "District", "Station Count"],
            [
                [rank, row["district"], row["number_of_stations"]]
                for rank, row in enumerate(districts_by_station_count, start=1)
            ],
        )
    )

    output_sections.append("\nAccessibility Score Ranking")
    output_sections.append(
        format_table(
            ["Rank", "District", "Accessibility Score"],
            [
                [rank, row["district"], row["accessibility_score"]]
                for rank, row in enumerate(accessibility_ranked, start=1)
            ],
        )
    )

    output_sections.append("\nMost Accessible District")
    output_sections.append(
        f"{most_accessible['district']} with "
        f"{most_accessible['number_of_stations']} transport stations"
    )

    output_text = "\n\n".join(output_sections)

    # Print all results to the console for quick inspection.
    print(output_text)

    # Save the same results to a text file for the report and portfolio.
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_FILE.write_text(output_text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
