# Vienna Housing & Transport Accessibility Analysis

Analyzing the relationship between housing prices and public transport accessibility across Vienna's districts using a graph-based data model.

## Overview

This project investigates whether Vienna districts with stronger public transport connectivity tend to have higher housing prices. Housing price and public transport station data are combined into a graph structure, allowing relationships between districts and transport access to be queried and analyzed directly — rather than through repeated joins across separate tables.

## Business Question

Do districts with better public transport accessibility command higher housing prices in Vienna — and how much of the price variation can accessibility actually explain?

## Data

| Dataset | Description |
|---|---|
| `housing_prices.csv` | Average housing price (EUR/m²) per district |
| `transport_stations.csv` | Public transport stations, type, and district |

Both datasets are joined on district to build a unified graph.

## Approach

1. **Graph construction** — Built a graph with `District` and `Station` node types connected via `LOCATED_IN` relationships (Python, Pandas, NetworkX). Resulting graph: 15 districts, 35 stations, 35 relationships.
2. **Querying & analysis** — Ran graph queries to rank districts by price and by accessibility (number of connected stations).
3. **Graph evolution** — Derived an accessibility score per district and classified districts into High/Medium/Low accessibility tiers, adding these back into the graph as new nodes and relationships (53 nodes, 50 relationships after evolution).
4. **Similarity analysis** — Converted each district into a normalized 2-feature vector (price, accessibility) and used cosine similarity to identify districts with comparable profiles.
5. **Visualization** — Produced the graph structure, a housing price comparison chart, an accessibility score chart, and a price-vs-accessibility scatter plot (Matplotlib).

## Key Findings

- **Innere Stadt** is both the most expensive district (€18,300/m²) and among the most accessible.
- Accessibility is **not concentrated in one area** — six districts share the top accessibility score, including much cheaper ones like **Donaustadt** (€5,900/m²).
- This shows accessibility is a real driver of housing attractiveness, but **not sufficient on its own** to explain price differences — other economic and geographic factors matter too.
- Similarity analysis grouped districts like **Favoriten** and **Donaustadt**, which share similar accessibility and affordability profiles.

## Tools

Python · Pandas · NetworkX · Matplotlib

## Repository Structure

```
├── data/raw/          # Source CSV datasets
├── src/                # Graph construction, querying, visualization, evolution scripts
├── results/            # Generated charts, query outputs, similarity results
├── report_notes/        # Supporting analysis notes
└── requirements.txt
```

## Running the Project

```bash
pip install -r requirements.txt
python src/build_graph.py       # constructs the knowledge graph
python src/analyze_graph.py     # runs queries and generates results
python src/visualize.py         # produces charts in results/
```

## Limitations & Future Work

This uses a small, education-scale dataset with a simplified accessibility metric (station count only). Extending it with official Vienna open data, travel-time-based accessibility, and demographic factors would give a more complete picture.
