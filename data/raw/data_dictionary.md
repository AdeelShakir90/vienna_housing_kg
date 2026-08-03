# Data Dictionary

This folder contains small sample datasets for the project **Knowledge Graph for Analyzing Housing Prices and Accessibility in Vienna**. The files are intended for portfolio and learning purposes, not as official statistical data.

## `housing_prices.csv`

| Column | Description | Example |
| --- | --- | --- |
| `district` | Name of a Vienna district included in the sample dataset. | `Leopoldstadt` |
| `avg_price_eur_m2` | Example average housing price in euros per square meter for the district. | `7600` |

## `transport_stations.csv`

| Column | Description | Example |
| --- | --- | --- |
| `station` | Name of a public transport station or stop in Vienna. | `Stephansplatz` |
| `district` | Vienna district where the station or stop is located. This can be linked to the `district` column in `housing_prices.csv`. | `Innere Stadt` |
| `transport_type` | Type of public transport represented by the station or stop. Allowed values are `U-Bahn`, `Tram`, and `Bus`. | `U-Bahn` |

## Notes

- The datasets are deliberately small so the Knowledge Graph can be built and explained clearly.
- District names are shared across both CSV files so they can be used as linking entities in a later graph model.
- Prices are realistic example values created for coursework and should not be treated as current market data.
