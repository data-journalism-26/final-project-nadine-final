import matplotlib.pyplot as plt
import pandas as pd

from config import DATA_PROCESSED, FIGURES_DIR


def plot_split_index() -> None:
  source = DATA_PROCESSED / "split_index_2015_2025.csv"
  if not source.exists():
    print("Missing split index file, cannot render figure.")
    return

  df = pd.read_csv(source)
  pivot = df.pivot(index="year", columns="series", values="value")
  plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.titlesize": 17,
    "axes.titleweight": "semibold",
    "axes.labelsize": 12,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
  })
  fig, ax = plt.subplots(figsize=(11.2, 6.1))
  fig.patch.set_facecolor("#fbfaf7")
  ax.set_facecolor("#fbfaf7")

  # Map internal series names to reader-facing labels
  label_map = {
    "all_traffic_deaths_index": "All traffic deaths",
    "cyclist_deaths_index": "Cyclist deaths",
  }

  colors = {
    "all_traffic_deaths_index": "#1f1f1f",
    "cyclist_deaths_index": "#d84f8f",
  }

  years = pivot.index
  last_year = years.max()
  first_year = years.min()

  ax.axvspan(2021, 2022, color="#d8d2c8", alpha=0.32, linewidth=0)
  ax.text(
    2021.5,
    129,
    "2022 marked\na new high",
    ha="center",
    va="top",
    fontsize=10,
    color="#777777",
  )

  ax.axhline(100, color="#b8b8b8", linewidth=0.9, linestyle=(0, (2, 3)), zorder=1)

  if "all_traffic_deaths_index" in pivot.columns:
    col = "all_traffic_deaths_index"
    ax.plot(
      years,
      pivot[col],
      color=colors[col],
      linewidth=1.8,
      marker="o",
      markersize=4,
      markerfacecolor="#fbfaf7",
      markeredgewidth=1.2,
      zorder=3,
    )

  if "cyclist_deaths_index" in pivot.columns:
    col = "cyclist_deaths_index"
    ax.plot(
      years,
      pivot[col],
      color=colors[col],
      linewidth=3.0,
      marker="o",
      markersize=4.8,
      markerfacecolor="#fbfaf7",
      markeredgewidth=1.5,
      zorder=4,
    )
    ax.scatter(
      [last_year],
      [pivot.loc[last_year, col]],
      s=86,
      color=colors[col],
      edgecolor="#fbfaf7",
      linewidth=1.4,
      zorder=5,
    )

  for col, y_offset in [
    ("cyclist_deaths_index", 1.5),
    ("all_traffic_deaths_index", -1.5),
  ]:
    if col not in pivot.columns:
      continue
    end_val = float(pivot.loc[last_year, col])
    label = label_map[col]
    pct_change = end_val - 100.0
    sign = "+" if pct_change >= 0 else "\u2212"
    pct_text = f"{sign}{abs(pct_change):.1f}%"
    ax.text(
      last_year + 0.25,
      end_val + y_offset,
      f"{label}\n{pct_text}",
      va="center",
      ha="left",
      fontsize=11.5,
      fontweight="bold" if col == "cyclist_deaths_index" else "normal",
      color=colors[col],
    )

  ax.set_title("Road deaths fell. Cyclist deaths did not.", loc="left", pad=30)
  ax.text(
    0,
    1.035,
    "Indexed to 2015 = 100. By 2025, overall traffic deaths were down 18.6%, while cyclist deaths were up 20.6%.",
    transform=ax.transAxes,
    ha="left",
    va="bottom",
    fontsize=12,
    color="#555555",
  )
  ax.text(
    0,
    -0.16,
    "Source: Destatis; annual fatalities indexed to 2015 = 100. 2025 figures are preliminary/estimated.",
    transform=ax.transAxes,
    ha="left",
    va="top",
    fontsize=10,
    color="#777777",
  )

  ax.set_xlabel("")
  ax.set_ylabel("Index")
  ax.set_xlim(first_year - 0.35, last_year + 1.35)
  ax.set_ylim(68, 132)
  ax.set_xticks(list(range(first_year, last_year + 1)))
  ax.set_yticks([70, 80, 90, 100, 110, 120, 130])
  ax.grid(axis="y", color="#ddd8d0", linewidth=0.7)
  ax.grid(axis="x", visible=False)
  ax.tick_params(axis="both", length=0, colors="#555555")
  for spine in ["top", "right", "left"]:
    ax.spines[spine].set_visible(False)
  ax.spines["bottom"].set_color("#c8c0b6")
  ax.spines["bottom"].set_linewidth(0.8)
  ax.margins(x=0)
  fig.subplots_adjust(left=0.08, right=0.83, top=0.78, bottom=0.2)

  FIGURES_DIR.mkdir(parents=True, exist_ok=True)
  out = FIGURES_DIR / "figure1_split_index.png"
  fig.savefig(out, dpi=220, bbox_inches="tight", facecolor=fig.get_facecolor())
  plt.close()
  print(f"Wrote figure: {out.name}")


def run() -> None:
  plot_split_index()
  plot_cyclist_types()


def plot_cyclist_types() -> None:
  source = DATA_PROCESSED / "cyclist_types_2015_2025.csv"
  if not source.exists():
    print("Missing cyclist types file, cannot render figure 2.")
    return

  df = pd.read_csv(source)
  pivot = df.pivot(index="year", columns="series", values="value")

  FIGURES_DIR.mkdir(parents=True, exist_ok=True)
  plt.figure(figsize=(8, 5))

  # Reader-facing label mapping
  label_map = {
    "killed_cyclists_total": "All killed cyclists",
    "killed_bicycle_without_motor": "Bicycle without motor",
    "killed_pedelec_users": "Pedelec users",
  }

  # Color choices: muted for non-pedelec, pink accent for pedelec
  colors = {
    "killed_cyclists_total": "#1f1f1f",
    "killed_bicycle_without_motor": "#9f1f63",
    "killed_pedelec_users": "#d84f8f",
  }

  last_year = pivot.index.max()
  first_year = pivot.index.min()

  for col in ["killed_bicycle_without_motor", "killed_cyclists_total", "killed_pedelec_users"]:
    y = pivot[col]
    lw = 3 if col == "killed_pedelec_users" else 2
    alpha = 1.0 if col == "killed_pedelec_users" else 0.9
    plt.plot(pivot.index, y, marker="o", linewidth=lw, label=label_map.get(col, col), color=colors.get(col), alpha=alpha)

    # Direct end label with final value and percent change from baseline
    start_val = float(pivot.loc[first_year, col])
    end_val = float(pivot.loc[last_year, col])
    pct = (end_val / start_val - 1) * 100
    label = f"{label_map.get(col)}: {int(end_val):,} ({pct:+.0f}% since {first_year})"
    plt.text(last_year + 0.15, end_val, label, va="center", fontsize=9, color=colors.get(col))

  plt.title("Cyclist deaths by type (2015–2025)")
  plt.xlabel("Year")
  plt.ylabel("Number of deaths")
  # Remove default legend; we use direct labels
  plt.xlim(first_year - 0.5, last_year + 1.2)
  plt.gca().yaxis.get_major_locator()
  plt.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.6)
  plt.tight_layout()

  out = FIGURES_DIR / "figure2_cyclist_types.png"
  plt.savefig(out, dpi=180)
  plt.close()
  print(f"Wrote figure: {out.name}")

if __name__ == "__main__":
  run()
