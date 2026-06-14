"""
Purpose:
    Generate realistic synthetic ticketing, customer, promotion, section,
    and web funnel data for an NBA revenue optimization analytics project.

Inputs:
    data/raw/clippers_games.csv if available; otherwise creates a fallback schedule.

Outputs:
    data/processed/dim_games.csv
    data/processed/dim_customers.csv
    data/processed/dim_sections.csv
    data/processed/dim_promotions.csv
    data/processed/fact_ticket_transactions.csv
    data/processed/fact_web_sessions.csv
"""

from pathlib import Path
import numpy as np
import pandas as pd

np.random.seed(42)

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

ARENA_CAPACITY = 18000


def load_or_create_games():
    games_path = RAW_DIR / "clippers_games.csv"

    if games_path.exists():
        games = pd.read_csv(games_path)
        games = games.head(41).copy()

        dim_games = pd.DataFrame({
            "game_id": range(1, len(games) + 1),
            "game_date": pd.to_datetime(games["GAME_DATE"]),
            "opponent": games["MATCHUP"].str.extract(r"vs\. ([A-Z]{3})|@ ([A-Z]{3})").bfill(axis=1)[0],
        })
    else:
        opponents = ["LAL", "GSW", "BOS", "NYK", "DAL", "DEN", "PHX", "SAC", "MIA", "MIL", "OKC", "SAS"]
        dates = pd.date_range("2025-10-20", periods=41, freq="4D")

        dim_games = pd.DataFrame({
            "game_id": range(1, 42),
            "game_date": dates,
            "opponent": np.random.choice(opponents, 41),
        })

    premium_opponents = {
        "LAL": 1.00,
        "GSW": 0.95,
        "BOS": 0.92,
        "NYK": 0.88,
        "DAL": 0.82,
        "DEN": 0.80,
        "PHX": 0.76,
        "MIL": 0.75,
        "OKC": 0.74,
        "SAC": 0.70,
    }

    dim_games["day_of_week"] = dim_games["game_date"].dt.day_name()
    dim_games["is_weekend"] = dim_games["day_of_week"].isin(["Friday", "Saturday", "Sunday"]).astype(int)
    dim_games["opponent_strength"] = dim_games["opponent"].map(premium_opponents)
    missing_strength = dim_games["opponent_strength"].isna()
    dim_games.loc[missing_strength, "opponent_strength"] = np.random.uniform(
        0.35,
        0.65,
        missing_strength.sum()
    )
    dim_games["arena_capacity"] = ARENA_CAPACITY

    return dim_games


def create_sections():
    return pd.DataFrame([
        {"section_id": 1, "section_name": "Courtside", "capacity": 500, "base_price": 550},
        {"section_id": 2, "section_name": "Club", "capacity": 2500, "base_price": 220},
        {"section_id": 3, "section_name": "Lower Bowl", "capacity": 6500, "base_price": 140},
        {"section_id": 4, "section_name": "Upper Bowl", "capacity": 7500, "base_price": 65},
        {"section_id": 5, "section_name": "Standing Room", "capacity": 1000, "base_price": 45},
    ])


def create_promotions():
    return pd.DataFrame([
        {"promotion_id": 0, "promotion_name": "No Promotion", "discount_percent": 0.00},
        {"promotion_id": 1, "promotion_name": "Family Pack", "discount_percent": 0.15},
        {"promotion_id": 2, "promotion_name": "Student Night", "discount_percent": 0.25},
        {"promotion_id": 3, "promotion_name": "Military Discount", "discount_percent": 0.20},
        {"promotion_id": 4, "promotion_name": "Limited Time Offer", "discount_percent": 0.10},
    ])


def create_customers(n_customers=25000):
    age_groups = ["18-24", "25-34", "35-44", "45-54", "55+"]
    income_brackets = ["<$50K", "$50K-$99K", "$100K-$149K", "$150K+"]
    zip_codes = ["90001", "90003", "90008", "90015", "90045", "90210", "90301", "90401", "90802"]

    customers = pd.DataFrame({
        "customer_id": range(1, n_customers + 1),
        "age_group": np.random.choice(age_groups, n_customers, p=[0.18, 0.32, 0.24, 0.16, 0.10]),
        "income_bracket": np.random.choice(income_brackets, n_customers, p=[0.25, 0.35, 0.25, 0.15]),
        "zip_code": np.random.choice(zip_codes, n_customers),
        "season_ticket_holder": np.random.binomial(1, 0.08, n_customers),
    })

    return customers


def generate_transactions(dim_games, dim_sections, dim_promotions, dim_customers):
    transactions = []
    transaction_id = 1

    channels = ["Website", "Mobile App", "Ticketmaster", "Box Office"]
    devices = ["Desktop", "Mobile", "Tablet"]

    for _, game in dim_games.iterrows():
        demand_score = 0.50 + 0.35 * game["opponent_strength"] + 0.10 * game["is_weekend"]
        demand_score = min(demand_score, 0.98)

        for _, section in dim_sections.iterrows():
            section_capacity = int(section["capacity"])
            section_demand_multiplier = {
                "Courtside": 0.92,
                "Club": 0.88,
                "Lower Bowl": 0.82,
                "Upper Bowl": 0.70,
                "Standing Room": 0.60,
            }[section["section_name"]]

            sell_through = np.clip(
                demand_score * section_demand_multiplier + np.random.normal(0, 0.05),
                0.35,
                0.99
            )

            seats_to_sell = int(section_capacity * sell_through)

            while seats_to_sell > 0:
                seats_purchased = min(np.random.choice([1, 2, 3, 4], p=[0.25, 0.45, 0.15, 0.15]), seats_to_sell)

                customer = dim_customers.sample(1).iloc[0]

                promotion_probability = 0.10
                if game["opponent_strength"] < 0.60:
                    promotion_probability = 0.35

                promotion_id = np.random.choice(
                    dim_promotions["promotion_id"],
                    p=[1 - promotion_probability, promotion_probability * .35, promotion_probability * .30,
                       promotion_probability * .15, promotion_probability * .20]
                )

                promo = dim_promotions[dim_promotions["promotion_id"] == promotion_id].iloc[0]

                dynamic_price = section["base_price"] * (
                    1 + 0.55 * game["opponent_strength"] + 0.12 * game["is_weekend"]
                )

                final_price = dynamic_price * (1 - promo["discount_percent"])
                final_price = round(max(final_price + np.random.normal(0, 8), 20), 2)

                days_before_game = np.random.randint(1, 120)
                purchase_date = game["game_date"] - pd.Timedelta(days=int(days_before_game))

                revenue = round(seats_purchased * final_price, 2)

                transactions.append({
                    "transaction_id": transaction_id,
                    "customer_id": customer["customer_id"],
                    "game_id": game["game_id"],
                    "section_id": section["section_id"],
                    "promotion_id": promotion_id,
                    "purchase_date": purchase_date.date().isoformat(),
                    "seats_purchased": seats_purchased,
                    "ticket_price": final_price,
                    "revenue": revenue,
                    "channel": np.random.choice(channels, p=[0.45, 0.35, 0.15, 0.05]),
                    "device": np.random.choice(devices, p=[0.35, 0.58, 0.07]),
                })

                transaction_id += 1
                seats_to_sell -= seats_purchased

    return pd.DataFrame(transactions)


def generate_web_sessions(dim_games):
    sessions = []
    session_id = 1

    sources = ["Paid Search", "Email", "Social", "Organic", "Direct"]
    devices = ["Desktop", "Mobile", "Tablet"]

    for _, game in dim_games.iterrows():
        visitors = int(25000 + 60000 * game["opponent_strength"] + 7000 * game["is_weekend"])

        for _ in range(visitors // 50):
            added_to_cart = np.random.binomial(1, 0.32 + 0.15 * game["opponent_strength"])
            checkout_started = np.random.binomial(1, 0.65) if added_to_cart else 0
            purchased = np.random.binomial(1, 0.78) if checkout_started else 0

            sessions.append({
                "session_id": session_id,
                "game_id": game["game_id"],
                "device": np.random.choice(devices, p=[0.35, 0.58, 0.07]),
                "source": np.random.choice(sources, p=[0.28, 0.24, 0.20, 0.18, 0.10]),
                "viewed_ticket_page": 1,
                "added_to_cart": added_to_cart,
                "checkout_started": checkout_started,
                "purchased": purchased,
            })

            session_id += 1

    return pd.DataFrame(sessions)


def main():
    dim_games = load_or_create_games()
    dim_sections = create_sections()
    dim_promotions = create_promotions()
    dim_customers = create_customers()

    fact_transactions = generate_transactions(dim_games, dim_sections, dim_promotions, dim_customers)
    fact_web_sessions = generate_web_sessions(dim_games)

    dim_games.to_csv(PROCESSED_DIR / "dim_games.csv", index=False)
    dim_sections.to_csv(PROCESSED_DIR / "dim_sections.csv", index=False)
    dim_promotions.to_csv(PROCESSED_DIR / "dim_promotions.csv", index=False)
    dim_customers.to_csv(PROCESSED_DIR / "dim_customers.csv", index=False)
    fact_transactions.to_csv(PROCESSED_DIR / "fact_ticket_transactions.csv", index=False)
    fact_web_sessions.to_csv(PROCESSED_DIR / "fact_web_sessions.csv", index=False)

    print("Generated revenue optimization dataset.")
    print(f"Games: {len(dim_games)}")
    print(f"Customers: {len(dim_customers)}")
    print(f"Ticket transactions: {len(fact_transactions)}")
    print(f"Web sessions: {len(fact_web_sessions)}")


if __name__ == "__main__":
    main()