# Limitations

Project: **Knowledge Graph for Analyzing Housing Prices and Accessibility in Vienna**

This project is designed as a university portfolio project, so several parts are intentionally simplified.

## Sample Datasets

The datasets are small sample datasets created for learning and demonstration purposes. They are not official housing market statistics or official public transport datasets.

This means the results should be interpreted as examples of Knowledge Graph analysis rather than conclusions about the real Vienna housing market.

## Limited Number of Districts

The project includes 15 Vienna districts, not all 23 districts.

This keeps the graph small and readable for a portfolio, but it limits the completeness of the analysis. A final real-world version should include all districts and a larger number of stations.

## Simplified Accessibility Score

The accessibility score is based only on the number of transport stations connected to a district.

This does not account for:

- Distance from housing locations to stations
- Travel time to the city center or other destinations
- Frequency of public transport service
- Station importance or network centrality
- Walking routes and barriers
- Differences between U-Bahn, Tram, and Bus capacity

The score is useful for demonstrating graph-based analysis, but it is not a full accessibility model.

## Simple Embedding Representation

The district vector representation uses only two normalized values:

```text
[normalized_avg_price_eur_m2, normalized_accessibility_score]
```

This is a simple embedding-style representation for learning purposes. It does not capture complex graph structure, semantic meaning, geographic distance, or transport network topology.

The project does not use Graph Neural Networks or deep learning embeddings. A more advanced version could explore graph embedding algorithms, richer node features, and larger datasets.
