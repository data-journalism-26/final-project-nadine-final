from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
FIGURES_DIR = PROJECT_ROOT / "figures"

# Baseline year for index figures.
BASE_YEAR = 2015

# Core years currently planned for the article.
START_YEAR = 2014
END_YEAR = 2025
