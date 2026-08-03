# Methodology

Project: **Knowledge Graph for Analyzing Housing Prices and Accessibility in Vienna**

This methodology describes how the project data is modeled, transformed into a Knowledge Graph, analyzed, and extended with simple similarity features.

## Node Types

### District

`District` nodes represent Vienna districts included in the sample housing dataset.

Main attributes:

- `label`: readable district name
- `type`: `District`
- `avg_price_eur_m2`: average housing price in euros per square meter
- `accessibility_score`: number of connected transport stations, added during KG evolution
- `accessibility_category`: derived category based on accessibility score

### Station

`Station` nodes represent public transport stations or stops.

Main attributes:

- `label`: readable station name
- `type`: `Station`
- `transport_type`: one of `U-Bahn`, `Tram`, or `Bus`

### AccessibilityCategory

`AccessibilityCategory` nodes represent derived accessibility groups.

Main attributes:

- `label`: `High`, `Medium`, or `Low`
- `type`: `AccessibilityCategory`

## Edge Types

### LOCATED_IN

The `LOCATED_IN` relationship connects a station to the district where it is located.

Direction:

`Station --> District`

This direction makes it possible to count incoming station relationships for each district.

### HAS_ACCESSIBILITY_CATEGORY

The `HAS_ACCESSIBILITY_CATEGORY` relationship connects a district to its derived accessibility category.

Direction:

`District --> AccessibilityCategory`

This relationship is added during the Knowledge Graph evolution step.

## Graph Schema

The initial graph schema contains two main entity types:

- `District`
- `Station`

The main relationship is:

- `Station --LOCATED_IN--> District`

The evolved graph adds:

- `AccessibilityCategory`
- `District --HAS_ACCESSIBILITY_CATEGORY--> AccessibilityCategory`

This schema supports analysis of how transport accessibility relates to housing price differences across districts.

## Accessibility Score

The accessibility score is a simple graph-derived metric.

Formula:

```text
accessibility_score = number of incoming LOCATED_IN edges from Station nodes
```

The score is interpreted as the number of transport stations connected to a district in the sample dataset.

Accessibility categories are assigned as follows:

| Accessibility Score | Category |
| --- | --- |
| `>= 3` | High |
| `== 2` | Medium |
| `<= 1` | Low |

This is a simplified measure of accessibility. It does not include distance, travel time, service frequency, walking routes, or network centrality.

## Similarity Analysis

The project includes a simple embedding-style representation for learning purposes.

Each district is represented as a two-value vector:

```text
[normalized_avg_price_eur_m2, normalized_accessibility_score]
```

The values are normalized so price and accessibility can be compared on a similar scale.

Cosine similarity is then calculated between all district vectors. For each district, the two most similar districts are identified.

This representation is intentionally simple. It is not a deep learning model and does not use Graph Neural Networks. Its purpose is to show how graph attributes can be transformed into numerical vectors for basic similarity analysis.
