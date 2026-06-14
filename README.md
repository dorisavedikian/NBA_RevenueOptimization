# 🏀 NBA Revenue Intelligence

> An end-to-end revenue analytics and business intelligence platform for professional sports organizations.

![Python](https://img.shields.io/badge/Python-3.11-blue)

![SQL](https://img.shields.io/badge/SQL-SQLite-green)

![Machine Learning](https://img.shields.io/badge/Machine%20Learning-scikit--learn-orange)

![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-yellow)

![GitHub](https://img.shields.io/badge/GitHub-Version%20Controlled-black)

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Business Problem](#business-problem)
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

NBA Revenue Intelligence is an end-to-end analytics platform that simulates the responsibilities of a Data Analyst supporting a professional sports organization.

The platform integrates Python, SQL, machine learning, and business intelligence to forecast ticket demand, optimize pricing strategies, evaluate marketing performance, monitor inventory, and generate executive recommendations for revenue optimization.

Rather than analyzing historical box scores or player statistics, this project focuses on the business operations behind professional sports organizations, including ticket sales, customer behavior, marketing funnels, and revenue forecasting.


## Key Features

- End-to-end ETL pipeline built with Python
- Synthetic enterprise ticketing simulation engine
- SQL dimensional data warehouse
- Executive KPI reporting layer
- K-Means game demand segmentation
- Revenue forecasting using regression models
- Executive recommendation engine
- Dashboard-ready dataset for Power BI
- One-click analytics pipeline

## Technology Stack

| Area | Technology |
|-------|------------|
| Programming | Python |
| Database | SQLite (PostgreSQL Ready) |
| Data Processing | pandas, NumPy |
| Machine Learning | scikit-learn |
| API | nba_api |
| Business Intelligence | Power BI |
| Version Control | Git & GitHub |

## Business Problem

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

![Architecture](docs/Images/architecture.png)

## Data Pipeline

The platform follows a modern analytics workflow:

```text
NBA Schedule
        │
        ▼
Python ETL
        │
        ▼
Enterprise Ticketing Simulation Engine
        │
        ▼
SQL Data Warehouse
        │
        ▼
Feature Engineering
        │
 ┌──────┴─────────┐
 ▼                ▼
K-Means       Regression
        │
        ▼
Executive KPI Engine
        │
        ▼
Recommendation Engine
        │
        ▼
Power BI
```

## Data Warehouse

The project uses a dimensional star schema designed for analytical workloads.

### Dimension Tables

- dim_games
- dim_customers
- dim_sections
- dim_promotions

### Fact Tables

- fact_ticket_transactions
- fact_web_sessions
- revenue_forecasts
- game_segments

This design separates descriptive business entities from transactional data to support scalable reporting and machine learning workflows.

## Machine Learning

The platform includes two supervised analytics workflows and one unsupervised workflow.

### K-Means Clustering

Games are segmented into:

- Premium Demand
- Standard Demand
- Promotion Opportunity
- Inventory Risk

### Regression Forecasting

Regression models predict:

- Ticket demand
- Revenue
- Sell-through rate
- Sellout probability

Forecasts are written back into the SQL warehouse for downstream reporting.

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

These datasets are designed for visualization in Power BI.

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
├── docs/
├── sql/
│   ├── schema/
│   ├── analytics/
│   └── tests/
│
├── src/
│   ├── analytics/
│   ├── etl/
│   ├── models/
│   ├── simulation/
│   └── warehouse/
│
├── dashboard/
├── notebooks/
├── tests/
├── run_pipeline.py
└── README.md
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

## Results

The project successfully demonstrates an end-to-end analytics workflow, including:

- ETL pipeline
- SQL data warehouse
- Executive KPI reporting
- Feature engineering
- K-Means segmentation
- Regression forecasting
- Recommendation engine

The final output is a dashboard-ready dataset that enables executives to make pricing, marketing, inventory, and revenue optimization decisions.

## Future Enhancements

- Snowflake data warehouse
- Docker deployment
- Streamlit executive dashboard
- Customer lifetime value modeling
- Dynamic pricing optimization
- Price elasticity analysis
- Propensity modeling

