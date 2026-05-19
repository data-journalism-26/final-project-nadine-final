import zipfile
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from config import DATA_PROCESSED, DATA_RAW, FIGURES_DIR


UNFALLATLAS_ZIP = DATA_RAW / "unfallatlas_mfdz_body.zip"
CRASH_TYPE_COUNTS = DATA_PROCESSED / "berlin_bicycle_crash_types_2024.csv"
FIGURE_SVG = FIGURES_DIR / "figure3_crash_types_berlin.svg"
FIGURE_PNG = FIGURES_DIR / "figure3_crash_types_berlin.png"
MAP_YEAR = 2024
BERLIN_STATE_CODE = 11

CRASH_TYPE_LABELS = {
  1: "Riding crash",
  2: "Turning crash",
  3: "Crossing/entering crash",
  4: "Pedestrian crossing crash",
  5: "Parked-vehicle crash",
  6: "Same-direction traffic crash",
  7: "Other crash",
}

HIGHLIGHT_TYPES = {2, 3}
HIGHLIGHT_COLOR = "#d84f8f"
OTHER_COLOR = "#dedede"
SUMMARY_OTHER_COLOR = "#dedede"
INK = "#111111"
MUTED = "#6f6a66"
PAPER = "#ffffff"


def _read_berlin_bicycle_crash_types() -> pd.DataFrame:
  if CRASH_TYPE_COUNTS.exists():
    return pd.read_csv(CRASH_TYPE_COUNTS)

  if not UNFALLATLAS_ZIP.exists():
    raise FileNotFoundError(
      f"Missing {UNFALLATLAS_ZIP}. Download the MFDZ Unfallatlas body.zip first."
    )

  usecols = ["UJAHR", "ULAND", "UTYP1", "IstRad"]
  frames = []
  with zipfile.ZipFile(UNFALLATLAS_ZIP) as archive:
    csv_names = [name for name in archive.namelist() if name.endswith(".csv")]
    for name in csv_names:
      with archive.open(name) as handle:
        df = pd.read_csv(handle, usecols=usecols)
      df = df[
        (df["UJAHR"] == MAP_YEAR)
        & (df["ULAND"] == BERLIN_STATE_CODE)
        & (df["IstRad"] == 1)
      ]
      if not df.empty:
        frames.append(df)

  crashes = pd.concat(frames, ignore_index=True)
  counts = (
    crashes["UTYP1"]
    .value_counts()
    .rename_axis("crash_type_code")
    .reset_index(name="count")
  )
  counts["label"] = counts["crash_type_code"].map(CRASH_TYPE_LABELS)
  counts["is_highlight"] = counts["crash_type_code"].isin(HIGHLIGHT_TYPES)
  counts = counts.sort_values("count", ascending=False).reset_index(drop=True)

  DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
  counts.to_csv(CRASH_TYPE_COUNTS, index=False)
  return counts


def plot_berlin_bicycle_crash_types() -> None:
  counts = _read_berlin_bicycle_crash_types()
  highlighted = int(counts.loc[counts["is_highlight"], "count"].sum())
  total = int(counts["count"].sum())
  highlight_share = highlighted / total
  counts["share"] = counts["count"] / total * 100

  colors = [HIGHLIGHT_COLOR if highlight else OTHER_COLOR for highlight in counts["is_highlight"]]
  label_colors = [INK if highlight else MUTED for highlight in counts["is_highlight"]]

  plt.rcParams.update({
    "font.family": "DejaVu Serif",
    "axes.titlesize": 21,
    "axes.labelsize": 11,
    "xtick.labelsize": 10.5,
    "ytick.labelsize": 11.5,
  })

  fig = plt.figure(figsize=(11.4, 6.4), facecolor=PAPER)
  fig.patch.set_facecolor(PAPER)

  fig.text(
    0.06,
    0.89,
    "More than half involve turning or\ncrossing situations",
    ha="left",
    va="top",
    fontsize=21,
    color=INK,
    fontweight="bold",
    linespacing=0.92,
  )
  summary_ax = fig.add_axes([0.06, 0.64, 0.88, 0.095])
  ax = fig.add_axes([0.23, 0.23, 0.71, 0.38])
  summary_ax.set_facecolor(PAPER)
  ax.set_facecolor(PAPER)

  y = range(len(counts))
  ax.barh(y, counts["share"], color=colors, height=0.9)

  for index, row in counts.iterrows():
    ax.text(
      row["share"] + 0.65,
      index,
      f"{row['share']:.1f}%",
      ha="left",
      va="center",
      fontsize=10.8,
      color=INK,
      fontweight="bold" if row["is_highlight"] else "normal",
    )

  ax.set_yticks(list(y))
  ax.set_yticklabels(counts["label"])
  for tick, color in zip(ax.get_yticklabels(), label_colors):
    tick.set_color(color)
    if color == INK:
      tick.set_fontweight("bold")

  ax.invert_yaxis()
  ax.set_xlim(0, 35)
  ax.set_xticks([0, 10, 20, 30])
  ax.set_xticklabels(["0%", "10%", "20%", "30%"])
  ax.grid(axis="x", color="#ededed", linewidth=0.5)
  ax.grid(axis="y", visible=False)
  ax.tick_params(axis="both", length=0, colors=MUTED)
  for spine in ["top", "right", "left", "bottom"]:
    ax.spines[spine].set_visible(False)

  other_share = 100 - highlight_share * 100
  summary_ax.barh([0], [highlight_share * 100], color=HIGHLIGHT_COLOR, height=0.86)
  summary_ax.barh([0], [other_share], left=[highlight_share * 100], color=SUMMARY_OTHER_COLOR, height=0.86)
  summary_ax.text(
    2,
    0,
    f"{highlight_share:.0%} turning or crossing/entering",
    ha="left",
    va="center",
    fontsize=12,
    color=PAPER,
    fontweight="bold",
  )
  summary_ax.text(
    98,
    0,
    f"{other_share:.0f}% other recorded crash types",
    ha="right",
    va="center",
    fontsize=12,
    color=INK,
    fontweight="bold",
  )
  summary_ax.set_xlim(0, 100)
  summary_ax.set_ylim(-0.5, 0.5)
  summary_ax.axis("off")
  FIGURES_DIR.mkdir(parents=True, exist_ok=True)
  fig.savefig(FIGURE_SVG, bbox_inches="tight", facecolor=fig.get_facecolor())
  fig.savefig(FIGURE_PNG, dpi=220, bbox_inches="tight", facecolor=fig.get_facecolor())
  plt.close(fig)
  print(f"Wrote figure: {FIGURE_SVG.name}")


if __name__ == "__main__":
  plot_berlin_bicycle_crash_types()
