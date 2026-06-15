from pathlib import Path


def test_required_project_files_exist():
    required_paths = [
        "main.py",
        "requirements.txt",
        "README.md",
        "src/config/paths.py",
        "src/simulation/ticket_sales.py",
        "src/etl/load.py",
        "src/warehouse/create_views.py",
        "src/analytics/feature_engineering.py",
        "src/models/kmeans.py",
        "src/models/regression.py",
    ]

    for path in required_paths:
        assert Path(path).exists(), f"Missing required path: {path}"
