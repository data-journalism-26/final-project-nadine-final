import pandas as pd

from config import BASE_YEAR, DATA_PROCESSED


def _series_index(df: pd.DataFrame, value_col: str, series_name: str) -> pd.DataFrame:
  subset = df[["year", value_col]].dropna().copy()
  base_values = subset.loc[subset["year"] == BASE_YEAR, value_col]
  if base_values.empty:
    return pd.DataFrame(columns=["year", "series", "value"])
  base = float(base_values.iloc[0])
  subset["series"] = series_name
  subset["value"] = subset[value_col].astype(float) / base * 100.0
  return subset[["year", "series", "value"]]


def build_split_index(traffic: pd.DataFrame, cyclists: pd.DataFrame) -> pd.DataFrame:
  left = _series_index(traffic, "killed_total", "all_traffic_deaths_index")
  right = _series_index(cyclists, "killed_cyclists_total", "cyclist_deaths_index")
  merged = pd.concat([left, right], ignore_index=True)
  merged = merged[(merged["year"] >= 2015) & (merged["year"] <= 2025)]
  return merged.sort_values(["series", "year"]).reset_index(drop=True)


def build_cyclist_types_long(cyclists: pd.DataFrame) -> pd.DataFrame:
  cols = [
    "killed_cyclists_total",
    "killed_bicycle_without_motor",
    "killed_pedelec_users",
  ]
  long_df = cyclists.melt(
    id_vars=["year"],
    value_vars=cols,
    var_name="series",
    value_name="value",
  )
  return long_df.sort_values(["year", "series"]).reset_index(drop=True)


def run() -> None:
  DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
  traffic_path = DATA_PROCESSED / "traffic_deaths_annual_clean.csv"
  cyclists_path = DATA_PROCESSED / "cyclist_fatalities_by_type_clean.csv"
  age_path = DATA_PROCESSED / "age_share_2025_clean.csv"
  crash_context_path = DATA_PROCESSED / "bicycle_crash_context_clean.csv"

  if not traffic_path.exists() or not cyclists_path.exists():
    print("Missing cleaned inputs. Run cleaning step first.")
    return

  traffic = pd.read_csv(traffic_path)
  cyclists = pd.read_csv(cyclists_path)

  split = build_split_index(traffic, cyclists)
  split.to_csv(DATA_PROCESSED / "split_index_2015_2025.csv", index=False)

  cyclist_types = build_cyclist_types_long(cyclists)
  cyclist_types.to_csv(DATA_PROCESSED / "cyclist_types_2015_2025.csv", index=False)

  if age_path.exists():
    pd.read_csv(age_path).to_csv(DATA_PROCESSED / "age_share_2025.csv", index=False)

  if crash_context_path.exists():
    pd.read_csv(crash_context_path).to_csv(
      DATA_PROCESSED / "bicycle_crash_context_2025.csv", index=False
    )

  print(f"Wrote chart-ready analysis outputs (base year: {BASE_YEAR}).")


if __name__ == "__main__":
  run()
