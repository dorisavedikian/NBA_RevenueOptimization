# 🏀 NBA Revenue Intelligence

End-to-End Sports Revenue Analytics Platform for professional sports organizations.

![Python](https://img.shields.io/badge/Python-3.11-blue)

![SQL](https://img.shields.io/badge/SQL-SQLite-green)

![Machine Learning](https://img.shields.io/badge/Machine%20Learning-scikit--learn-orange)

![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-yellow)

![GitHub](https://img.shields.io/badge/GitHub-Version%20Controlled-black)

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Business Context](#business-context)
- [Data Source & Simulation](#data-source--simulation)
- [System Architecture](#system-architecture)
- [Data Pipeline](#data-pipeline)
- [Dimensional Data Warehouse](#dimensional-data-warehouse)
- [Machine Learning](#machine-learning)
- [Business Intelligence](#business-intelligence)
- [Executive Decision Support](#executive-decision-support)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Results](#results)
- [Future Enhancements](#future-enhancements)

---

## Overview

NBA Revenue Intelligence is an end-to-end analytics platform that simulates the ticketing and revenue analytics workflows of a professional sports organization.

The platform combines real NBA schedule data with a realistic enterprise ticketing simulation to model ticket transactions, customer behavior, marketing campaigns, pricing strategies, inventory management, and web conversion funnels. It then applies data engineering, dimensional modeling, machine learning, and business intelligence techniques to generate executive insights that support revenue optimization.

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

Professional sports organizations rely heavily on analytics to maximize ticket revenue while maintaining fan engagement.

Leadership teams need to answer questions such as:

- Which games are likely to sell out?
- Which games require promotional campaigns?
- Should ticket prices increase or decrease?
- Which customer segments generate the most revenue?
- Where do customers abandon the purchasing process?
- What revenue should we expect for upcoming games?

This project demonstrates how an analytics platform can transform raw operational data into actionable business intelligence that supports pricing, inventory management, marketing, forecasting, and executive decision-making.

## Data Source & Simulation

Professional sports organizations do not publicly release ticketing, pricing, customer, or marketing data. To demonstrate an end-to-end revenue analytics workflow, this project combines real NBA schedule data with a realistic synthetic business layer that simulates ticket transactions, customer behavior, promotions, inventory, and web funnel activity.

The simulation was intentionally designed to mirror the types of operational data available to a professional sports organization's ticketing and business intelligence teams.

This approach enables the development of production-style data engineering pipelines, SQL data warehouses, machine learning models, forecasting workflows, and executive dashboards without relying on proprietary business data.

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

## Platform Components

The platform is organized into modular components:

- **Simulation Engine** – Generates realistic ticketing, customer, and marketing data.
- **ETL Layer** – Extracts, transforms, and loads data into the warehouse.
- **Dimensional Data Warehouse** – Stores transactional and dimensional data in a star schema.
- **Feature Engineering** – Produces model-ready datasets.
- **Machine Learning** – Performs demand segmentation and revenue forecasting.
- **Business Intelligence Layer** – Generates KPIs, recommendations, and dashboard-ready views.

## Data Pipeline

The platform follows a modern analytics workflow:

```text
NBA API
      │
      ▼
Simulation Engine
      │
      ▼
ETL Pipeline
      │
      ▼
Dimensional Data Warehouse
      │
      ▼
Feature Engineering
      │
 ┌─────┴─────────┐
 ▼               ▼
K-Means     Regression
      │
      ▼
KPI Engine
      │
      ▼
Recommendation Engine
      │
      ▼
Power BI Dashboard
```

## Dimensional Data Warehouse

The project uses a dimensional star schema designed for analytical workloads.

### Dimension Tables

- dim_customers
- dim_games
- dim_promotions
- dim_sections

### Fact Tables

- executive_kpis
- executive_recommendations
- fact_ticket_transactions
- fact_web_sessions
- game_segments
- model_dataset
- revenue_forecasts

This design separates descriptive business entities from transactional data to support scalable reporting and machine learning workflows.

## Machine Learning

The platform includes both unsupervised and supervised machine learning models designed to support ticketing strategy and revenue optimization.

### K-Means Clustering

Games are segmented into business demand profiles based on pricing, revenue, inventory, and customer behavior. These clusters help identify pricing opportunities, inventory risk, and games that may benefit from additional marketing or promotional efforts.

Segments include:

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

The analytics layer produces dashboard-ready SQL views for executive reporting.

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

The resulting datasets are consumed by Power BI to provide interactive dashboards for executives and business stakeholders.

## Executive Decision Support

Rather than simply producing reports, the platform generates business recommendations.

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
├── data/
│   ├── raw/
│   ├── external/
│   └── processed/
│
├── dashboard/
│   ├── powerbi/
│   └── screenshots/
│
├── docs/
│   ├── images/
│   ├── Architecture.md
│   ├── BusinessCase.md
│   └── DataDictionary.md
│
├── output/
│   └── figures/
│
├── sql/
│   ├── analytics/
│   ├── schema/
│   └── tests/
│
├── src/
│   │
│   ├── analytics/
│   │   ├── feature_engineering.py
│   │   ├── kpi_engine.py
│   │   └── recommendation_engine.py
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   ├── paths.py
│   │   └── settings.py
│   │
│   ├── etl/
│   │   └── load.py
│   │
│   ├── models/
│   │   ├── kmeans.py
│   │   └── regression.py
│   │
│   ├── simulation/
│   │   └── ticket_sales.py
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── helpers.py
│   │   └── logger.py
│   │
│   ├── visualization/
│   │   ├── cluster_plots.py
│   │   ├── forecast_plots.py
│   │   ├── revenue_plots.py
│   │   └── funnel_plots.py
│   │
│   ├── warehouse/
│   │   └── create_views.py
│   │
│   └── __init__.py
│
├── tests/
│   ├── test_etl.py
│   ├── test_models.py
│   ├── test_database.py
│   └── test_pipeline.py
│
├── .gitignore
├── LICENSE
├── main.py
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

The completed platform demonstrates a full analytics workflow representative of a modern sports business intelligence team. Starting with real NBA schedule data, the pipeline generates enterprise-scale operational data, builds a dimensional Dimensional Data Warehouse, engineers analytical features, trains machine learning models, and produces executive-ready datasets for dashboarding and decision support.

The project showcases practical experience in data engineering, SQL development, predictive analytics, business intelligence, and software engineering while emphasizing how analytics can drive pricing, marketing, inventory, and revenue decisions.

## Pipeline Outputs

The analytics pipeline produces:

- SQLite dimensional warehouse
- Machine learning feature dataset
- Game demand segments
- Revenue forecasts
- Executive KPIs
- Executive recommendations
- Dashboard-ready SQL views

## Future Enhancements

### Data Platform

- PostgreSQL migration
- Snowflake warehouse
- Apache Airflow orchestration

### Machine Learning

- Price elasticity modeling
- Customer lifetime value
- Propensity modeling
- Churn prediction

### Business Intelligence

- Executive reporting
- Automated KPI alerts

### Deployment

- Docker
- CI/CD
- Cloud deployment

## Acknowledgements

This project uses the open-source nba_api package to retrieve publicly available NBA schedule and team information.

All ticketing, customer, pricing, and marketing data used throughout the project are synthetically generated for educational and portfolio purposes.