# Iranian Research Paper & Thesis Scraper (ganj.irandoc.ac.ir)

A small Python project for collecting metadata about Iranian research papers and theses from **Ganj – IranDoc** ([ganj.irandoc.ac.ir](https://ganj.irandoc.ac.ir/)) and saving the results to CSV for analysis.

This repository currently contains:

- A Selenium-based scraper (`main.py`) that queries the IranDoc search UI year-by-year and writes `data.csv`.
- A simple CSV “cleaner” (`test.py`) that rewrites a CSV and replaces empty fields with `N/A`.
- Example output artifacts (`data.csv`, `cleaned_file.csv`, `cleaned_file2.csv`) and a sample Excel file (`Book1.xlsx`).

> Note: The scraper is written as a runnable script (not a packaged library) and it currently uses hard-coded parameters (keyword + year range). Configuring it means editing `main.py`.

---

## Table of contents

- [What this project does](#what-this-project-does)
- [Repository structure](#repository-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [1) Run the scraper](#1-run-the-scraper)
  - [2) Clean the CSV](#2-clean-the-csv)
- [Configuration (edit in code)](#configuration-edit-in-code)
- [Output files & schemas](#output-files--schemas)
  - [`data.csv` (raw scrape output)](#datacsv-raw-scrape-output)
  - [`cleaned_file.csv` / `cleaned_file2.csv` (cleaned output)](#cleaned_filecsv--cleaned_file2csv-cleaned-output)
- [Encoding / Persian text notes](#encoding--persian-text-notes)
- [Limitations](#limitations)
- [Troubleshooting](#troubleshooting)
- [Legal & ethical disclaimer](#legal--ethical-disclaimer)
- [License](#license)
- [Suggested next improvements](#suggested-next-improvements)

---

## What this project does

1. Opens IranDoc’s search page with a predefined query.
2. Scrapes result “cards” (title/subject + metadata like year, university, contributors).
3. Loops **year-by-year** and (when needed) **page-by-page** for larger result sets.
4. Exports the collected metadata as UTF‑8 CSV.

The goal is to create a dataset you can explore in Excel / Python / R (e.g., trends by year, university, supervisor, etc.).

---

## Repository structure

The repo is intentionally small and script-driven:

- `main.py` — Selenium scraper. Produces `data.csv`.
- `test.py` — CSV cleaner utility that rewrites a CSV and fills missing values with `N/A`.
- `readdata.py` — Present (currently empty).
- `data.csv` — Example/previous scrape output produced by `main.py`.
- `cleaned_file.csv`, `cleaned_file2.csv` — Example cleaned CSV outputs.
- `Book1.xlsx` — Sample spreadsheet artifact (not used by the scripts).
- `LICENSE` — MIT License.

---

## Requirements

### Runtime

- **Python 3.x**
- **Google Chrome** (installed)
- **ChromeDriver** compatible with your Chrome version
- Python packages:
  - `selenium`
  - `beautifulsoup4`

> The script calls `webdriver.Chrome()` directly, so the simplest setup is to place `chromedriver.exe` on your `PATH` (or otherwise ensure Selenium can locate it).

### OS notes

This repository works fine on Windows. The examples below use **Windows PowerShell**.

---

## Installation

1. Create and activate a virtual environment (recommended).
2. Install Python dependencies.
3. Install ChromeDriver and ensure it’s available on `PATH`.

Example (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install selenium beautifulsoup4
```

ChromeDriver setup (high level):

- Check your Chrome version in `chrome://settings/help`.
- Download the matching ChromeDriver.
- Put `chromedriver.exe` somewhere on your `PATH`.

---

## Usage

### 1) Run the scraper

`main.py` launches Chrome, runs the search, loops through years, and writes `data.csv` in the repo root.

```powershell
python .\main.py
```

What to expect:

- A Chrome window will open and navigate across result pages/years.
- The script prints progress, including the year being scraped and how many cards were extracted.
- When finished, Chrome closes and `data.csv` is written.

### 2) Clean the CSV

`test.py` reads `data.csv` and writes a cleaned file (by default `cleaned_file2.csv`).

```powershell
python .\test.py
```

---

## Configuration (edit in code)

The scraper is currently configured by editing constants inside `main.py`.

Key parameters you’ll likely edit:

- **Search keyword**: hard-coded inside the `url` string as a URL-encoded value.
  - Current keyword in the repo URL is Persian: `بیوانفورماتیک` (bioinformatics), URL-encoded.
- **Year range**:
  - `start_year = 1382`
  - Loop continues while `start_year <= 1403`
- **Paging**:
  - `pg_number` is incremented when there are more than 100 results.
  - The script attempts to track totals using a `dupl` list.
- **Results per page**:
  - The URL currently uses `results_per_page=4`.

Browser behavior:

- The driver is created with `webdriver.Chrome()` with no extra options.
  - That means it will use Selenium’s default Chrome session (not headless).

---

## Output files & schemas

### `data.csv` (raw scrape output)

`main.py` writes a single CSV named `data.csv` (UTF‑8).

The columns are:

- Fixed columns:
  - `subject`
  - `type`
  - `course`
  - `category`
  - `year`
  - `university`
- Variable contributor columns (the script expands these based on the maximum observed counts):
  - `student_1`, `student_2`, …
  - `professor_1`, `professor_2`, …
  - `moshaver_1`, `moshaver_2`, …

Notes on scraped values:

- Missing values are often written as `N/A`.
- Contributor roles are inferred by checking for Persian role keywords in the card:
  - student: roles containing `پدید`
  - professor/supervisor: roles containing `راهنما`
  - advisor/consultant: roles containing `مشاور`

### `cleaned_file.csv` / `cleaned_file2.csv` (cleaned output)

This repo includes two example cleaned outputs. The cleaner script (`test.py`) does the following:

- Reads an input CSV using UTF‑8.
- Replaces empty fields with `N/A`.
- Writes to an output CSV using `csv.QUOTE_MINIMAL`.

By default (as committed), `test.py` uses:

- Input: `data.csv`
- Output: `cleaned_file2.csv`

> Important: the cleaner does not change column names or restructure data; it only fills empty cells. If you need a “normalized” table (e.g., one contributor per row), that’s not implemented in this repo yet.

---

## Encoding / Persian text notes

- All scripts use **UTF‑8** when reading/writing CSV.
- If you open CSVs in Excel and see garbled Persian characters, import the file and explicitly choose **UTF‑8**.
  - In many Excel versions: **Data → From Text/CSV → File Origin: UTF‑8**.

---

## Limitations

This project uses Selenium to scrape a live site and is subject to typical scraping constraints:

- **Fragile selectors**: if IranDoc changes DOM structure, class names, or Angular bindings, scraping may break.
- **Dynamic loading timing**: the script uses waits and sleeps; slow connections may require adjustments.
- **Result count assumptions**: there is logic around thresholds like 100 results and page calculations, which may not generalize to all queries.
- **CAPTCHA / bot defenses**: if the site adds protections, automation may be blocked.

---

## Troubleshooting

Common issues and fixes:

1. **`selenium.common.exceptions.WebDriverException` / ChromeDriver not found**
   - Make sure `chromedriver.exe` is installed and available on `PATH`.
   - Ensure ChromeDriver version matches your installed Chrome.

2. **Script opens Chrome but extracts 0 cards**
   - The site layout may have changed.
   - Try increasing waits or re-checking the card selectors used in `extract_card_data()`.

3. **Unicode / Persian text looks broken in Excel**
   - Import the CSV and select UTF‑8 rather than double-click opening.

4. **The script runs very slowly**
   - Selenium is inherently slower than pure HTTP scraping.
   - Consider narrowing the year range or keyword.

---

## Legal & ethical disclaimer

This project is intended for educational and research use.

- Always respect **IranDoc’s Terms of Service** and applicable laws.
- Avoid aggressive crawling (high concurrency or rapid requests) that could impact service availability.
- Don’t collect or republish sensitive/personal data.

You are responsible for how you run and use this scraper.

---

## License

MIT License. See [`LICENSE`](LICENSE).

---

## Suggested next improvements

These are not implemented in the current codebase (this README does not change code), but they’re common enhancements:

- Add a `requirements.txt` (or `pyproject.toml`) for reproducible installs.
- Move hard-coded parameters (keyword, years, output file) to CLI arguments (e.g., `argparse`).
- Add robust explicit waits and resilient selectors.
- Normalize contributors into a relational-friendly format (one person per row) for analysis.
- Add a small test suite and CI checks.
