import json
from datetime import UTC, datetime
from pathlib import Path

import requests

from config import DATA_RAW


RAW_SOURCES = {
  "destatis_traffic_deaths_annual.csv": {
    "url": "https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Verkehrsunfaelle/_Grafik/_Interaktiv/Daten/verkehrsunfaelle-getoetete-jahr.csv?__blob=value&v=20",
    "description": "Annual road traffic deaths in Germany (Destatis interactive data).",
  },
  "destatis_cyclist_fatalities_2015_2025.csv": {
    "url": "https://www.destatis.de/DE/Presse/Pressemitteilungen/Grafiken/Newsroom/2026/Interaktiv/Daten/20260427-fahrradunfaelle.csv?__blob=value&v=1",
    "description": "Cyclist fatalities by type (total, bicycle without motor, pedelec).",
  },
  "destatis_press_release_pd26_n025_461.html": {
    "url": "https://www.destatis.de/DE/Presse/Pressemitteilungen/2026/04/PD26_N025_461.html",
    "description": "Press release containing age-65+ shares and bicycle crash context statements.",
  },
  "unfallatlas_mfdz_body.zip": {
    "url": "https://data.mfdz.de/destatis_Unfalldaten/body.zip",
    "description": "Unfallatlas open data bundle with point-level road crashes with personal injury, 2016-2024.",
  },
}


def ensure_directories() -> None:
  DATA_RAW.mkdir(parents=True, exist_ok=True)


def report_raw_inventory() -> dict[str, bool]:
  inventory = {}
  for filename in RAW_SOURCES:
    inventory[filename] = (DATA_RAW / filename).exists()
  return inventory


def download_source(filename: str, url: str) -> tuple[bool, str]:
  target = DATA_RAW / filename
  try:
    response = requests.get(url, timeout=45)
    response.raise_for_status()
    target.write_bytes(response.content)
    return True, f"downloaded ({len(response.content)} bytes)"
  except requests.RequestException as exc:
    if target.exists():
      return False, f"download failed, using existing local file ({exc})"
    return False, f"download failed ({exc})"


def write_source_registry(status_log: dict[str, dict[str, str]]) -> None:
  payload = {
    "generated_at_utc": datetime.now(UTC).isoformat(),
    "sources": status_log,
  }
  (DATA_RAW / "source_registry.json").write_text(
    json.dumps(payload, indent=2, ensure_ascii=True), encoding="utf-8"
  )


def run() -> None:
  ensure_directories()
  status_log: dict[str, dict[str, str]] = {}

  print("Downloading raw data sources:")
  for filename, meta in RAW_SOURCES.items():
    ok, status = download_source(filename, meta["url"])
    marker = "OK" if ok else "WARN"
    print(f"- {filename}: {marker} ({status})")
    status_log[filename] = {
      "url": meta["url"],
      "description": meta["description"],
      "status": status,
      "present_locally": str((DATA_RAW / filename).exists()),
    }

  write_source_registry(status_log)

  inventory = report_raw_inventory()
  print("\nRaw data inventory status:")
  for filename, exists in inventory.items():
    marker = "OK" if exists else "MISSING"
    print(f"- {filename}: {marker}")


if __name__ == "__main__":
  run()
