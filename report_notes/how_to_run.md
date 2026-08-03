# How to Run the Project

Project: **Knowledge Graph for Analyzing Housing Prices and Accessibility in Vienna**

These steps assume you are running commands from the project root folder:

```text
vienna_housing_kg/
```

## 1. Install Requirements

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## 2. Build the Knowledge Graph

Run:

```bash
python src/build_knowledge_graph.py
```

This script:

- Loads `data/raw/housing_prices.csv`
- Loads `data/raw/transport_stations.csv`
- Creates District and Station nodes
- Adds `LOCATED_IN` relationships
- Saves `results/vienna_housing_graph.gpickle`
- Saves `results/figures/knowledge_graph.png`

## 3. Run Graph Queries

Run:

```bash
python src/kg_queries.py
```

This script:

- Loads `results/vienna_housing_graph.gpickle`
- Finds the most expensive and cheapest districts
- Counts transport stations per district
- Computes accessibility scores
- Saves `results/tables/query_results.txt`

## 4. Create Visualizations

Run:

```bash
python src/create_visualizations.py
```

This script:

- Loads the housing price dataset
- Loads the saved graph
- Creates price and accessibility charts
- Creates a price-versus-accessibility scatter plot
- Saves `results/tables/district_accessibility_summary.csv`
- Saves figures in `results/figures/`

## 5. Generate Insights

Run:

```bash
python src/kg_insights.py
```

This script:

- Loads `results/vienna_housing_graph.gpickle`
- Finds the most expensive highly accessible district
- Finds the cheapest highly accessible district
- Calculates average price by accessibility score
- Saves `results/tables/project_insights.txt`

## 6. Evolve the KG and Create Simple Vectors

Run:

```bash
python src/kg_evolution_and_embeddings.py
```

This script:

- Loads `results/vienna_housing_graph.gpickle`
- Adds `accessibility_score` to District nodes
- Adds `accessibility_category` to District nodes
- Adds AccessibilityCategory nodes
- Adds `HAS_ACCESSIBILITY_CATEGORY` relationships
- Saves `results/vienna_housing_graph_evolved.gpickle`
- Creates simple district vectors
- Computes cosine similarity between districts
- Saves `results/tables/district_vectors.csv`
- Saves `results/tables/district_similarity.txt`

## Recommended Run Order

```bash
python src/build_knowledge_graph.py
python src/kg_queries.py
python src/create_visualizations.py
python src/kg_insights.py
python src/kg_evolution_and_embeddings.py
```

This order rebuilds the graph first and then regenerates the query results, figures, insights, evolved graph, vectors, and similarity report.
