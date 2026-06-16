# 🏀 NBA Revenue Intelligence

An end-to-end sports analytics platform that simulates NBA ticketing operations using Python, SQL, machine learning, and business intelligence to support revenue optimization and executive decision-making.

![CI](https://github.com/dorisavedikian/NBA_RevenueIntelligence/actions/workflows/ci.yml/badge.svg)

![Python](https://img.shields.io/badge/Python-3.11-blue)

![SQL](https://img.shields.io/badge/SQL-SQLite-green)

![Machine Learning](https://img.shields.io/badge/Machine%20Learning-scikit--learn-orange)

![License](https://img.shields.io/badge/license-MIT-blue)

![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-yellow)

## Overview

NBA Revenue Intelligence is an end-to-end analytics platform that simulates the ticketing and revenue analytics workflows of a professional sports organization.

The project demonstrates the complete analytics lifecycle—from data ingestion and ETL through SQL warehousing, feature engineering, predictive modeling, KPI reporting, and dashboard-ready outputs—using technologies commonly found in modern analytics organizations.

## Key Features

- End-to-end ETL pipeline built with Python
- Synthetic enterprise ticketing simulation engine
- SQL dimensional data warehouse
- Executive KPI reporting layer
- K-Means game demand segmentation
- Revenue forecasting using regression models
- Executive recommendation engine
- Dashboard-ready SQL views and datasets for Power BI.
- One-click analytics pipeline

## Technology Stack

| Category | Technologies |
|-----------|--------------|
| Programming Language | Python 3 |
| Data Engineering | Custom ETL Pipeline |
| Database | SQLite (Designed for PostgreSQL Migration) |
| SQL | Star Schema, SQL Views, Analytics Queries |
| Data Processing | pandas, NumPy |
| Machine Learning | scikit-learn (K-Means Clustering, Linear Regression) |
| Data Source | nba_api (NBA Schedule & Team Data) |
| Business Intelligence | Power BI |
| Software Engineering | Modular Python Package, Virtual Environments |
| Version Control | Git & GitHub |

## Business Context

Professional sports organizations rely on analytics to optimize ticket pricing, maximize revenue, improve fan engagement, and forecast demand.

This project demonstrates how modern analytics techniques can transform operational ticketing data into actionable business intelligence.

## Data Source & Simulation

### Real Data

- NBA schedule and game information (via `nba_api`)
- Teams
- Opponents
- Game dates

### Simulated Business Data

- Ticket transactions
- Customer demographics
- Arena seating inventory
- Dynamic ticket pricing
- Marketing promotions
- Website sessions
- Purchase funnel events
- Revenue
- Sell-through
- Inventory

## System Architecture

![Architecture](docs/images/architecture.png)

## Star Schema

The project uses a dimensional star schema designed for analytical workloads.

### Dimension Tables

- dim_games
- dim_customers
- dim_sections
- dim_promotions

### Fact Tables

- fact_ticket_transactions
- fact_web_sessions

![Star Schema](docs/images/star_schema.png)

### Analytical Outputs

- model_dataset
- game_segments
- revenue_forecasts
- executive_kpis
- executive_recommendations

This design separates descriptive business entities from transactional data to support scalable reporting and machine learning workflows.

## Analytics Pipeline

![Pipeline](docs/images/pipeline.png)

## Sample Outputs

The analytics pipeline automatically generates executive datasets and visualizations that support downstream reporting and business intelligence.

<table>
  <tr>
    <td align="center">
      <b>Revenue by Opponent</b><br>
      <img src="output/figures/revenue_by_opponent.png" width="400">
    </td>
    <td align="center">
      <b>Forecast vs Actual Revenue</b><br>
      <img src="output/figures/forecast_vs_actual.png" width="400">
    </td>
  </tr>
  <tr>
    <td align="center">
      <b>Game Demand Segments</b><br>
      <img src="output/figures/game_segments.png" width="400">
    </td>
    <td align="center">
      <b>Ticket Purchase Funnel</b><br>
      <img src="output/figures/checkout_funnel.png" width="400">
    </td>
  </tr>
</table>

## Machine Learning

The platform includes both unsupervised and supervised machine learning models designed to support ticketing strategy and revenue optimization.

### K-Means Clustering

Segments games into demand profiles based on pricing, revenue, inventory, and customer behavior.

- Premium Demand
- Standard Demand
- Promotion Opportunity
- Inventory Risk

### Regression Forecasting

Regression models predict key business metrics including:

- Ticket demand
- Revenue
- Sell-through rate
- Sellout probability

Forecasts are written back into the Dimensional Data Warehouse, allowing downstream reporting tools and dashboards to compare historical performance with future projections.

## Business Intelligence

Core KPIs include:

- Total Revenue
- Tickets Sold
- Sell-through Rate
- Inventory Remaining
- Average Ticket Price
- Funnel Conversion
- Cart Abandonment
- Forecast Revenue
- Sellout Probability

## Executive Decision Support

Example outputs include:

| Scenario | Recommendation |
|----------|----------------|
| Premium Demand | Increase premium seating prices |
| Promotion Opportunity | Launch targeted marketing campaign |
| Inventory Risk | Increase advertising and promotions |
| High Checkout Abandonment | Improve checkout experience |

The objective is to help executives translate analytics into measurable business decisions.

## Project Structure

```text
NBA_RevenueIntelligence/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── dashboard/
│   ├── powerbi/
│   └── screenshots/
│
├── data/
│   ├── analytics/
│   │   ├── executive_kpis.csv
│   │   ├── executive_recommendations.csv
│   │   ├── game_segments.csv
│   │   ├── model_dataset.csv
│   │   └── revenue_forecasts.csv
│   │
│   ├── external/
│   ├── raw/
│   └── warehouse/
│       ├── dim_customers.csv
│       ├── dim_games.csv
│       ├── dim_promotions.csv
│       ├── dim_sections.csv
│       ├── fact_ticket_transactions.csv
│       ├── fact_web_sessions.csv
│       └── nba_revenue_optimization.sqlite
│
├── docs/
│   ├── images/
│   ├── architecture.md
│   ├── business_case.md
│   ├── business_requirements.md
│   └── data_dictionary.md
│
├── notebooks/
│
├── output/
│   └── figures/
│       ├── checkout_funnel.png
│       ├── forecast_vs_actual.png
│       ├── game_segments.png
│       └── revenue_by_opponent.png
│
├── sql/
│   ├── analytics/
│   ├── schema/
│   │   └── create_views.sql
│   └── tests/
│       └── qa_checks.sql
│
├── src/
│   ├── analytics/
│   ├── config/
│   ├── etl/
│   ├── models/
│   ├── simulation/
│   ├── utils/
│   ├── visualization/
│   └── warehouse/
│
├── tests/
│   ├── test_analytics.py
│   ├── test_analytics_sql.py
│   ├── test_config.py
│   ├── test_database.py
│   ├── test_outputs.py
│   ├── test_project_structure.py
│   ├── test_simulation.py
│   └── test_sql_directory.py
│
├── .gitignore
├── LICENSE
├── main.py
├── pyproject.toml
├── README.md
└── requirements.txt
```

## Installation

Clone the repository:

```bash
git clone https://github.com/dorisavedikian/NBA_RevenueIntelligence.git
```

Navigate into the project:

```bash
cd NBA_RevenueIntelligence
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

macOS/Linux

```bash
source .venv/bin/activate
```

Windows

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the pipeline:

```bash
python main.py
```

Running `main.py` executes the complete analytics pipeline, including data generation, ETL, warehouse construction, feature engineering, machine learning, KPI generation, and executive recommendations.

## Results

The completed platform demonstrates an end-to-end analytics workflow representative of a modern sports business intelligence team.
