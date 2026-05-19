# Spring on Two Wheels

**Final project — Data Journalism, MDS, Spring 2026**  
**Author:** Nadine Daum  
**Date:** 19 May 2026  

Article: [Spring on Two Wheels](https://rawcdn.githack.com/data-journalism-26/final-project-nadine-final/5af0b976f36848ee365d47d85064c5304cfa48b0/spring-on-two-wheels.html)

## Project summary

This project is a data journalism article about a mobility paradox in Germany: pedelecs have made cycling easier, longer and more accessible, especially for older riders, while cyclist fatalities have not followed the broader decline in road deaths.

It combines national fatality data, age and crash-context statistics, Berlin crash-type data, and a practical weather check. The project does not argue that pedelecs are inherently dangerous. It examines where official statistics show a safety gap, and which street situations make that gap visible.

## Final output

The final article is:

```text
spring-on-two-wheels.html
```

It includes three original visual elements:

- Figure 1: overall road deaths and cyclist deaths indexed to 2015;
- Figure 2: the changing fatality mix between conventional bicycles and pedelec users;
- Figure 3: Berlin bicycle-involved injury crashes by recorded crash type, with a small reader reveal interaction.

## Data sources

The project uses:

- **Destatis** traffic accident statistics for national road deaths and cyclist fatalities;
- **Destatis press release PD26_N025_461** for 2025 cyclist, age and crash-context figures;
- **Unfallatlas / MFDZ open data** for Berlin bicycle-involved injury crashes in 2024;
- **Fahrrad-Unfallorte** as a public-facing reference for Berlin crash-type categories;
- **Open-Meteo / DWD API** for the practical weather card.

A local source registry is stored in:

```text
data/raw/source_registry.json
```

## Reproducibility

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

Run the full pipeline from the project root:

```bash
python scripts/run_pipeline.py
```

The pipeline downloads or reads the raw sources, cleans the data, creates chart-ready files, and exports the figures used in the article.

Open the article locally:

```bash
open spring-on-two-wheels.html
```

On systems without the `open` command, open `spring-on-two-wheels.html` manually in a browser.

## Repository structure

```text
spring-on-two-wheels.html     Final article
assets/                       CSS, JavaScript and images
data/raw/                     Original downloaded or stored data
data/processed/               Cleaned and chart-ready data
figures/                      Exported figures
scripts/                      Acquisition, cleaning, analysis and visualization code
requirements.txt              Python dependencies
```

## AI Note

AItools (Gemini, Github Copilot, and ChatGpt) were used to support coding, debugging, wording refinement, and documentation checks. The story angle, data selection, final decisions, interpretation, visual review and final editorial responsibility remain my own.
