# Project Inventory

Project: **Knowledge Graph for Analyzing Housing Prices and Accessibility in Vienna**

This inventory lists the datasets, scripts, generated outputs, figures, tables, and reports currently included in the portfolio project. It also maps each component to the learning outcomes supported by the work.

## Learning Outcome Key

- **LO1:** Understanding core Knowledge Graph concepts and terminology.
- **LO4:** Representing domain knowledge as entities and relationships.
- **LO5:** Designing a simple graph schema with node and edge types.
- **LO6:** Preparing and structuring data for Knowledge Graph construction.
- **LO7:** Implementing a Knowledge Graph with Python tools.
- **LO8:** Querying, analyzing, and extracting information from graph data.
- **LO9:** Interpreting graph-based results for a real-world use case.
- **LO11:** Communicating insights from Knowledge Graph analysis.
- **LO12:** Creating a reproducible project structure and workflow.

## Inventory Table

| File | Purpose | Related LO |
| --- | --- | --- |
| `README.md` | Introduces the project goal, planned data, tools, and learning outcome connections. | LO1, LO4, LO5, LO11, LO12 |
| `data/raw/housing_prices.csv` | Sample dataset containing Vienna districts and average housing prices per square meter. | LO4, LO6, LO9, LO12 |
| `data/raw/transport_stations.csv` | Sample dataset containing transport stations, districts, and transport types. | LO4, LO6, LO9, LO12 |
| `data/raw/data_dictionary.md` | Explains the meaning of all dataset columns and how the datasets can be linked. | LO1, LO5, LO6, LO12 |
| `src/build_knowledge_graph.py` | Loads CSV data, creates District and Station nodes, adds `LOCATED_IN` relationships, saves the graph, and creates the first graph visualization. | LO4, LO5, LO6, LO7, LO12 |
| `src/kg_queries.py` | Queries the graph for expensive and cheap districts, transport station counts, accessibility scores, and most accessible district. | LO7, LO8, LO9, LO11 |
| `src/create_visualizations.py` | Creates bar charts, a scatter plot, and a district-level accessibility summary table. | LO7, LO8, LO9, LO11, LO12 |
| `src/kg_insights.py` | Generates short textual insights from graph-derived accessibility and price results. | LO8, LO9, LO11 |
| `src/kg_evolution_and_embeddings.py` | Evolves the graph with accessibility attributes, category nodes, category relationships, and simple vector similarity analysis. | LO5, LO7, LO8, LO9, LO11 |
| `results/vienna_housing_graph.gpickle` | Saved initial NetworkX Knowledge Graph containing districts, stations, attributes, and `LOCATED_IN` edges. | LO4, LO5, LO7, LO12 |
| `results/vienna_housing_graph_evolved.gpickle` | Saved evolved Knowledge Graph containing accessibility scores, accessibility categories, and `HAS_ACCESSIBILITY_CATEGORY` relationships. | LO5, LO7, LO8, LO12 |
| `results/figures/knowledge_graph.png` | Visual overview of District and Station nodes with different colors. | LO4, LO5, LO7, LO11 |
| `results/figures/district_prices_bar_chart.png` | Bar chart comparing average housing prices across districts. | LO8, LO9, LO11 |
| `results/figures/accessibility_score_bar_chart.png` | Bar chart comparing station-based accessibility scores across districts. | LO8, LO9, LO11 |
| `results/figures/price_vs_accessibility_scatter.png` | Scatter plot comparing accessibility score with average housing price for each district. | LO8, LO9, LO11 |
| `results/tables/query_results.txt` | Text report containing graph query results and accessibility rankings. | LO8, LO9, LO11, LO12 |
| `results/tables/district_accessibility_summary.csv` | District-level table combining price, station count, and accessibility score. | LO6, LO8, LO9, LO12 |
| `results/tables/project_insights.txt` | Automatically generated textual summary of selected project insights. | LO8, LO9, LO11 |
| `results/tables/district_vectors.csv` | Simple embedding-style vector representation for each district using normalized price and accessibility score. | LO7, LO8, LO9 |
| `results/tables/district_similarity.txt` | Cosine similarity report showing the top two most similar districts for each district. | LO8, LO9, LO11 |
| `report_notes/project_inventory.md` | Inventory report documenting project components, outputs, and learning outcome coverage. | LO1, LO11, LO12 |

## Datasets Used

| File | Purpose | Related LO |
| --- | --- | --- |
| `data/raw/housing_prices.csv` | Provides district-level average housing prices used as District node attributes and analysis values. | LO4, LO6, LO9 |
| `data/raw/transport_stations.csv` | Provides Station nodes and links stations to District nodes through `LOCATED_IN` relationships. | LO4, LO5, LO6 |

## Python Scripts Created

| File | Purpose | Related LO |
| --- | --- | --- |
| `src/build_knowledge_graph.py` | Builds and saves the initial Knowledge Graph from CSV data. | LO4, LO5, LO6, LO7 |
| `src/kg_queries.py` | Performs graph queries and saves query results. | LO7, LO8, LO9 |
| `src/create_visualizations.py` | Creates visual summaries and a district accessibility summary table. | LO7, LO8, LO9, LO11 |
| `src/kg_insights.py` | Creates automated textual insight summaries. | LO8, LO9, LO11 |
| `src/kg_evolution_and_embeddings.py` | Adds graph evolution features and simple embedding-style similarity analysis. | LO5, LO7, LO8, LO9 |

## Generated Outputs

| File | Purpose | Related LO |
| --- | --- | --- |
| `results/vienna_housing_graph.gpickle` | Initial saved Knowledge Graph. | LO4, LO5, LO7, LO12 |
| `results/vienna_housing_graph_evolved.gpickle` | Evolved graph with accessibility categories and derived relationships. | LO5, LO7, LO8, LO12 |

## Figures and Charts

| File | Purpose | Related LO |
| --- | --- | --- |
| `results/figures/knowledge_graph.png` | Network visualization of the Knowledge Graph. | LO4, LO5, LO11 |
| `results/figures/district_prices_bar_chart.png` | Visual comparison of average housing prices by district. | LO8, LO9, LO11 |
| `results/figures/accessibility_score_bar_chart.png` | Visual comparison of transport accessibility by district. | LO8, LO9, LO11 |
| `results/figures/price_vs_accessibility_scatter.png` | Visual analysis of the relationship between housing price and accessibility. | LO8, LO9, LO11 |

## Tables and Text Reports

| File | Purpose | Related LO |
| --- | --- | --- |
| `results/tables/query_results.txt` | Saved graph query results. | LO8, LO9, LO11 |
| `results/tables/district_accessibility_summary.csv` | Combined district price and accessibility table. | LO6, LO8, LO9, LO12 |
| `results/tables/project_insights.txt` | Automatically generated written insights. | LO8, LO9, LO11 |
| `results/tables/district_vectors.csv` | Simple district vector table for similarity analysis. | LO7, LO8, LO9 |
| `results/tables/district_similarity.txt` | Similar district recommendations based on cosine similarity. | LO8, LO9, LO11 |

## Useful Missing Files for Final Portfolio Submission

| Suggested File | Purpose | Related LO |
| --- | --- | --- |
| `requirements.txt` | Lists required Python packages such as `pandas`, `networkx`, and `matplotlib` for reproducibility. | LO7, LO12 |
| `report_notes/final_report_outline.md` | Provides a structured outline for the final written portfolio report. | LO1, LO9, LO11 |
| `report_notes/methodology.md` | Explains the graph schema, node types, edge types, and analysis workflow in prose. | LO1, LO4, LO5, LO11 |
| `report_notes/limitations.md` | Documents that the datasets are small sample datasets and not official market data. | LO9, LO11 |
| `report_notes/how_to_run.md` | Gives step-by-step commands for rebuilding the graph, queries, figures, insights, and evolved graph. | LO7, LO12 |
| `results/tables/schema_summary.csv` | Summarizes node types, edge types, and key attributes in a compact table. | LO1, LO5, LO11 |
| `data/processed/` cleaned dataset files | Stores any cleaned or merged datasets if the workflow is expanded beyond raw sample data. | LO6, LO12 |
