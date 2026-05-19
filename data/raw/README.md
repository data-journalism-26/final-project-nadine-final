# Raw Data Notes

This folder stores untouched source files downloaded by `scripts/acquisition.py`.

Current automated sources:

- `destatis_traffic_deaths_annual.csv`: annual road traffic deaths in Germany.
- `destatis_cyclist_fatalities_2015_2025.csv`: cyclist fatalities by bicycle type.
- `destatis_press_release_pd26_n025_461.html`: Destatis press release used for age and crash-context metrics.
- `unfallatlas_mfdz_body.zip`: Unfallatlas / MFDZ open data bundle for road crashes with personal injury.

`source_registry.json` is generated on each acquisition run and records the source URL, description, download status and local availability.
