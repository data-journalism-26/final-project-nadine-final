from acquisition import run as run_acquisition
from analysis import run as run_analysis
from cleaning import run as run_cleaning
from crash_type_visualization import plot_berlin_bicycle_crash_types
from visualization import run as run_visualization


def run() -> None:
  print("Step 1/5: acquisition")
  run_acquisition()

  print("Step 2/5: cleaning")
  run_cleaning()

  print("Step 3/5: analysis")
  run_analysis()

  print("Step 4/5: visualization")
  run_visualization()

  print("Step 5/5: crash-type visualization")
  plot_berlin_bicycle_crash_types()

  print("Pipeline scaffold completed.")


if __name__ == "__main__":
  run()
