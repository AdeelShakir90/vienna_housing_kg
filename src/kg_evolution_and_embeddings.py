from itertools import combinations
from math import sqrt
from pathlib import Path
import pickle

import pandas as pd


# Resolve paths relative to the project root so the script can be run from
# different working directories.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = PROJECT_ROOT / "results"
TABLES_DIR = RESULTS_DIR / "tables"

INPUT_GRAPH_FILE = RESULTS_DIR / "vienna_housing_graph.gpickle"
EVOLVED_GRAPH_FILE = RESULTS_DIR / "vienna_housing_graph_evolved.gpickle"
SIMILARITY_FILE = TABLES_DIR / "district_similarity.txt"
VECTORS_FILE = TABLES_DIR / "district_vectors.csv"


def load_graph():
    """Load the existing Knowledge Graph from disk."""
    with INPUT_GRAPH_FILE.open("rb") as file:
        return pickle.load(file)


def save_graph(graph):
    """Save the evolved Knowledge Graph with new attributes and relationships."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    with EVOLVED_GRAPH_FILE.open("wb") as file:
        pickle.dump(graph, file, protocol=pickle.HIGHEST_PROTOCOL)


def get_district_nodes(graph):
    """Return all District nodes and their attributes."""
    return [
        (node, data)
        for node, data in graph.nodes(data=True)
        if data.get("type") == "District"
    ]


def count_station_edges(graph, district_node):
    """Count incoming LOCATED_IN edges from Station nodes to one District."""
    station_count = 0

    for source_node, _, edge_data in graph.in_edges(district_node, data=True):
        source_type = graph.nodes[source_node].get("type")
        relationship = edge_data.get("relationship")

        if source_type == "Station" and relationship == "LOCATED_IN":
            station_count += 1

    return station_count


def categorize_accessibility(accessibility_score):
    """Convert a numeric accessibility score into a simple category."""
    if accessibility_score >= 3:
        return "High"
    if accessibility_score == 2:
        return "Medium"
    return "Low"


def evolve_graph(graph):
    """Add accessibility attributes and category relationships to the graph."""
    for district_node, district_data in get_district_nodes(graph):
        accessibility_score = count_station_edges(graph, district_node)
        accessibility_category = categorize_accessibility(accessibility_score)
        category_node = f"accessibility_category:{accessibility_category}"

        # Add new derived attributes directly to the District node.
        district_data["accessibility_score"] = accessibility_score
        district_data["accessibility_category"] = accessibility_category

        # Add one category node per category value and connect districts to it.
        graph.add_node(
            category_node,
            label=accessibility_category,
            type="AccessibilityCategory",
        )
        graph.add_edge(
            district_node,
            category_node,
            relationship="HAS_ACCESSIBILITY_CATEGORY",
        )

    return graph


def normalize(value, minimum, maximum):
    """Normalize a value to the range 0 to 1."""
    if maximum == minimum:
        return 0.0

    return (value - minimum) / (maximum - minimum)


def build_district_vectors(graph):
    """
    Create a simple embedding-style vector for each District.

    This is a transparent learning representation based on two normalized
    graph attributes. It is not a deep learning model and does not use Graph
    Neural Networks.
    """
    district_rows = []

    for district_node, data in get_district_nodes(graph):
        district_rows.append(
            {
                "node_id": district_node,
                "district": data["label"],
                "avg_price_eur_m2": data["avg_price_eur_m2"],
                "accessibility_score": data["accessibility_score"],
            }
        )

    min_price = min(row["avg_price_eur_m2"] for row in district_rows)
    max_price = max(row["avg_price_eur_m2"] for row in district_rows)
    min_score = min(row["accessibility_score"] for row in district_rows)
    max_score = max(row["accessibility_score"] for row in district_rows)

    for row in district_rows:
        row["normalized_avg_price_eur_m2"] = normalize(
            row["avg_price_eur_m2"], min_price, max_price
        )
        row["normalized_accessibility_score"] = normalize(
            row["accessibility_score"], min_score, max_score
        )
        row["vector"] = [
            row["normalized_avg_price_eur_m2"],
            row["normalized_accessibility_score"],
        ]

    return district_rows


def cosine_similarity(vector_a, vector_b):
    """Compute cosine similarity between two numeric vectors."""
    dot_product = sum(a * b for a, b in zip(vector_a, vector_b))
    magnitude_a = sqrt(sum(a * a for a in vector_a))
    magnitude_b = sqrt(sum(b * b for b in vector_b))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


def find_top_similar_districts(district_vectors):
    """Find the top two most similar districts for every district."""
    similarity_scores = {row["district"]: [] for row in district_vectors}

    for row_a, row_b in combinations(district_vectors, 2):
        similarity = cosine_similarity(row_a["vector"], row_b["vector"])
        similarity_scores[row_a["district"]].append((row_b["district"], similarity))
        similarity_scores[row_b["district"]].append((row_a["district"], similarity))

    top_matches = {}
    for district, matches in similarity_scores.items():
        top_matches[district] = sorted(
            matches,
            key=lambda item: item[1],
            reverse=True,
        )[:2]

    return top_matches


def save_vectors(district_vectors):
    """Save district vector data to CSV for inspection and reporting."""
    rows_for_csv = []

    for row in district_vectors:
        rows_for_csv.append(
            {
                "district": row["district"],
                "avg_price_eur_m2": row["avg_price_eur_m2"],
                "accessibility_score": row["accessibility_score"],
                "normalized_avg_price_eur_m2": round(
                    row["normalized_avg_price_eur_m2"], 6
                ),
                "normalized_accessibility_score": round(
                    row["normalized_accessibility_score"], 6
                ),
            }
        )

    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows_for_csv).to_csv(VECTORS_FILE, index=False)


def save_similarity_results(top_matches):
    """Save top two district similarity matches as a readable text report."""
    lines = [
        "District Similarity Results",
        "===========================",
        "",
        "Simple vector representation: "
        "[normalized_avg_price_eur_m2, normalized_accessibility_score]",
        "Cosine similarity was used to compare district vectors.",
        "This is an embedding-style learning representation, not a deep learning model.",
        "",
    ]

    for district, matches in top_matches.items():
        formatted_matches = ", ".join(
            f"{match_district} ({similarity:.4f})"
            for match_district, similarity in matches
        )
        lines.append(f"{district}: {formatted_matches}")

    output_text = "\n".join(lines)
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    SIMILARITY_FILE.write_text(output_text + "\n", encoding="utf-8")

    return output_text


def main():
    graph = load_graph()

    # Part A: evolve the KG with derived accessibility attributes and category
    # relationships.
    evolved_graph = evolve_graph(graph)
    save_graph(evolved_graph)

    # Part B: create a simple two-feature district representation and compare
    # districts with cosine similarity. This is intentionally simple for KG
    # learning purposes and does not use Graph Neural Networks.
    district_vectors = build_district_vectors(evolved_graph)
    top_matches = find_top_similar_districts(district_vectors)
    save_vectors(district_vectors)
    similarity_text = save_similarity_results(top_matches)

    category_counts = {}
    for _, data in get_district_nodes(evolved_graph):
        category = data["accessibility_category"]
        category_counts[category] = category_counts.get(category, 0) + 1

    print("KG Evolution and Simple Embedding-Style Representation Complete")
    print("-------------------------------------------------------------")
    print(f"Evolved graph saved to: {EVOLVED_GRAPH_FILE}")
    print(f"District vectors saved to: {VECTORS_FILE}")
    print(f"District similarity results saved to: {SIMILARITY_FILE}")
    print("")
    print("Accessibility categories added:")
    for category, count in sorted(category_counts.items()):
        print(f"- {category}: {count} districts")
    print("")
    print(similarity_text)


if __name__ == "__main__":
    main()
