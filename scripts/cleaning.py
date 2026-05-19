import re
from pathlib import Path

import pandas as pd

from config import DATA_PROCESSED, DATA_RAW


def _read_semicolon_csv(path: str | Path) -> pd.DataFrame:
  return pd.read_csv(path, sep=";")


def _to_float(value: object) -> float | None:
  if pd.isna(value):
    return None
  if isinstance(value, (int, float)):
    return float(value)
  text = str(value).strip().replace("\xa0", "").replace(" ", "")
  text = text.replace("%", "")
  if "," in text and "." not in text:
    text = text.replace(",", ".")
  try:
    return float(text)
  except ValueError:
    return None


def _to_int_count(value: object) -> int | None:
  if pd.isna(value):
    return None
  text = str(value).strip().replace("\xa0", "").replace(" ", "")
  digits = re.sub(r"[^0-9]", "", text)
  if digits == "":
    return None
  return int(digits)


def clean_traffic_deaths() -> pd.DataFrame:
  source = DATA_RAW / "destatis_traffic_deaths_annual.csv"
  if not source.exists():
    return pd.DataFrame()
  df = _read_semicolon_csv(source)
  renamed = df.rename(columns={"Jahr": "year", "Getötete": "killed_total"})
  renamed["year"] = pd.to_numeric(renamed["year"], errors="coerce")
  renamed["killed_total"] = renamed["killed_total"].map(_to_int_count)
  renamed = renamed.dropna(subset=["year", "killed_total"])
  renamed["year"] = renamed["year"].astype(int)
  renamed["killed_total"] = renamed["killed_total"].astype(int)
  renamed = renamed[["year", "killed_total"]]
  return renamed.sort_values("year").reset_index(drop=True)


def clean_cyclist_fatalities_by_type() -> pd.DataFrame:
  source = DATA_RAW / "destatis_cyclist_fatalities_2015_2025.csv"
  if not source.exists():
    return pd.DataFrame()
  df = _read_semicolon_csv(source)
  renamed = df.rename(
    columns={
      "Jahr": "year",
      "Fahrräder insgesamt": "killed_cyclists_total",
      "Fahrräder ohne Hilfsmotor": "killed_bicycle_without_motor",
      "Pedelecs": "killed_pedelec_users",
    }
  )
  renamed["year"] = pd.to_numeric(renamed["year"], errors="coerce")
  for col in [
    "killed_cyclists_total",
    "killed_bicycle_without_motor",
    "killed_pedelec_users",
  ]:
    renamed[col] = renamed[col].map(_to_int_count)
  renamed = renamed.dropna(subset=["year", "killed_cyclists_total"])
  renamed["year"] = renamed["year"].astype(int)
  for col in [
    "killed_cyclists_total",
    "killed_bicycle_without_motor",
    "killed_pedelec_users",
  ]:
    renamed[col] = renamed[col].astype(int)
  renamed = renamed[
    [
      "year",
      "killed_cyclists_total",
      "killed_bicycle_without_motor",
      "killed_pedelec_users",
    ]
  ]
  return renamed.sort_values("year").reset_index(drop=True)


def _extract_raw(html: str, pattern: str) -> str | None:
  match = re.search(pattern, html, flags=re.IGNORECASE | re.DOTALL)
  if not match:
    return None
  return match.group(1)


def clean_press_release_metrics() -> tuple[pd.DataFrame, pd.DataFrame]:
  source = DATA_RAW / "destatis_press_release_pd26_n025_461.html"
  if not source.exists():
    return pd.DataFrame(), pd.DataFrame()

  html = source.read_text(encoding="utf-8", errors="ignore")
  normalized = html.replace("\xa0", " ")

  age_share = pd.DataFrame(
    [
      {
        "group": "all_killed_cyclists",
        "share_65_plus": _to_float(
          _extract_raw(
          normalized,
          r"(\d+,\d+)\s*%\s*der\s*t[öo]dlich\s*verungl[üu]ckten\s*Fahrrad",
          )
        ),
      },
      {
        "group": "killed_bicycle_without_motor",
        "share_65_plus": _to_float(
          _extract_raw(
          normalized,
          r"bei\s*t[öo]dlich\s*Verungl[üu]ckten\s*mit\s*Fahrr[äa]dern\s*ohne\s*Hilfsmotor\s*bei\s*(\d+,\d+)\s*%",
          )
        ),
      },
      {
        "group": "killed_pedelec_users",
        "share_65_plus": _to_float(
          _extract_raw(
          normalized,
          r"waren\s*(\d+,\d+)\s*%\s*der\s*get[öo]teten\s*Pedelec-Fahrenden",
          )
        ),
      },
    ]
  )

  crash_context = pd.DataFrame(
    [
      {
        "metric": "bicycle_injury_crashes_total",
        "value": _to_int_count(
          _extract_raw(
          normalized,
          r"([0-9][0-9\s\.\xa0]{2,})\s*Fahrradunf[äa]lle\s*mit\s*Personenschaden",
          )
        ),
      },
      {
        "metric": "bicycle_injury_crashes_two_party_share_pct",
        "value": _to_float(
          _extract_raw(normalized, r"An\s*einem\s*Gro[ßs]teil\s*\((\d+,\d+)\s*%\)")
        ),
      },
      {
        "metric": "bicycle_injury_crashes_with_car_share_pct",
        "value": _to_float(
          _extract_raw(
            normalized,
            r"In\s*(\d+,\d+)\s*%\s*der\s*F[äa]lle\s*war\s*dies\s*eine\s*Autofahrerin",
          )
        ),
      },
      {
        "metric": "bicycle_injury_crashes_with_car_count",
        "value": _to_int_count(
          _extract_raw(
            normalized,
            r"Autofahrer\s*\(([0-9\s\.]+)\s*Unf[äa]lle\)",
          )
        ),
      },
    ]
  )

  age_share["share_65_plus"] = age_share["share_65_plus"].astype(float)
  crash_context["value"] = crash_context["value"].astype(float)

  return age_share, crash_context
  return df


def run() -> None:
  DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

  traffic_deaths = clean_traffic_deaths()
  cyclist_types = clean_cyclist_fatalities_by_type()
  age_share, crash_context = clean_press_release_metrics()

  if traffic_deaths.empty:
    print("No traffic deaths raw file found yet.")
  else:
    traffic_deaths.to_csv(DATA_PROCESSED / "traffic_deaths_annual_clean.csv", index=False)
    print("Wrote cleaned file: traffic_deaths_annual_clean.csv")

  if cyclist_types.empty:
    print("No cyclist by-type raw file found yet.")
  else:
    cyclist_types.to_csv(
      DATA_PROCESSED / "cyclist_fatalities_by_type_clean.csv", index=False
    )
    print("Wrote cleaned file: cyclist_fatalities_by_type_clean.csv")

  if age_share.empty:
    print("No press-release age share metrics found yet.")
  else:
    age_share.to_csv(DATA_PROCESSED / "age_share_2025_clean.csv", index=False)
    print("Wrote cleaned file: age_share_2025_clean.csv")

  if crash_context.empty:
    print("No press-release crash context metrics found yet.")
  else:
    crash_context.to_csv(DATA_PROCESSED / "bicycle_crash_context_clean.csv", index=False)
    print("Wrote cleaned file: bicycle_crash_context_clean.csv")


if __name__ == "__main__":
  run()
