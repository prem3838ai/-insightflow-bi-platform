# InsightFlow — Business Intelligence & Automated Reporting Platform

A portfolio-ready interactive BI dashboard built with **Python, Pandas, Plotly, and Streamlit**. Explore sales performance, filter transactions, inspect product/region trends, generate an executive summary, and download filtered reports. The included dataset is synthetic demo data.

## Features

- Executive KPI cards: revenue, profit, profit margin, orders, customers, units, average order value.
- Interactive monthly revenue/profit trend and regional revenue breakdown.
- Product and category performance charts plus region summary.
- Sidebar filters for date, region, category, and sales channel.
- Upload your own CSV and validate required columns.
- Searchable transaction explorer.
- Download filtered transactions, monthly summary, and executive Markdown report.
- Reusable analytics functions with automated pytest tests.

## Preview

Run locally with the steps below. Add a screenshot of your running app to `docs/` and link it here when you publish your repository.

## Project structure

```text
.
├── app/streamlit_app.py       # Streamlit user interface
├── src/bi_platform/           # Data validation and analytics logic
├── data/sample/sales_data.csv # Synthetic sample sales dataset (900 rows)
├── tests/                     # Unit tests
├── .streamlit/config.toml     # Theme and server config
├── requirements.txt
├── pytest.ini
├── .env.example
├── .gitignore
└── README.md
```

## Requirements

- Python 3.10–3.12 recommended
- pip and Git
- Internet access for installing dependencies

## Run locally

### 1. Download or clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/insightflow-bi-platform.git
cd insightflow-bi-platform
```

If you downloaded the ZIP, extract it and open a terminal in the extracted folder.

### 2. Create a virtual environment

**Windows PowerShell**
```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Start the dashboard

```bash
streamlit run app/streamlit_app.py
```

Streamlit normally opens `http://localhost:8501` in your browser. The app loads the sample CSV automatically. Upload a CSV from the sidebar to analyze your own data.

## CSV schema for uploads

Required columns (case-insensitive; spaces in column names are normalized):

| Column | Meaning | Example |
|---|---|---|
| `order_date` | Order date | `2025-03-14` |
| `region` | Sales region | `West` |
| `product` | Product name | `Monitor 27` |
| `category` | Product category | `Electronics` |
| `quantity` | Units sold | `2` |
| `revenue` | Net sales amount | `620.00` |
| `cost` | Total cost | `390.00` |

Optional: `order_id`, `customer_id`, `sales_channel`, `unit_price`, `discount_pct`, `profit`. Missing `profit` is calculated as revenue minus cost; missing IDs/channels receive safe defaults. Dates that cannot be parsed are dropped.

**Data note:** the included records are randomly generated and do not represent a real company. Currency is intentionally unspecified; use one currency per uploaded file.

## Run tests

```bash
pytest
```

## Deploy free with Streamlit Community Cloud

1. Create a GitHub repository named `insightflow-bi-platform` (or another name).
2. Upload/push the complete contents of this project to the repository root. Ensure `app/`, `src/`, `data/`, `tests/`, `requirements.txt`, and `README.md` are at the root level.
3. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/) with GitHub and authorize repository access.
4. Select **Create app**, choose your repository and branch (usually `main`).
5. Set **Main file path** to `app/streamlit_app.py`.
6. Deploy. Streamlit installs packages from `requirements.txt`; the sample data path is resolved from the project tree.
7. Open the app URL and test the filters and CSV exports. Redeploy after pushing updates.

No secrets or API keys are required for the current version. Never commit real credentials or private customer data.

## Push to GitHub

```bash
git init
git add .
git commit -m "Build InsightFlow BI dashboard"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/insightflow-bi-platform.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username. If Git says the remote already exists, update it with `git remote set-url origin <repository-url>`.

### Upload from an Android phone

1. Extract the ZIP with your file manager or an archive app.
2. On GitHub, create a new repository.
3. Open the repository and use **Add file → Upload files** in a mobile browser; select the extracted files/folders if your browser supports folder selection.
4. If folder upload is awkward on mobile, use GitHub Codespaces: create a Codespace, upload/extract the ZIP in the workspace, then run `git add .`, `git commit`, and `git push`.
5. Deploy the repository on Streamlit Community Cloud using the steps above.

## Design and analytics notes

- Revenue = sum of transaction revenue.
- Profit = sum of profit; if absent, row-level profit is calculated as revenue minus cost.
- Profit margin = total profit / total revenue × 100.
- Average order value = total revenue / distinct order IDs.
- Monthly trend groups transactions by calendar month.

These definitions assume each row is a transaction line. If your source stores one order across multiple product lines, distinct order count is used to avoid counting each line as a separate order.

## Limitations and future extensions

This is a focused portfolio project, not a governed enterprise BI warehouse. Potential next steps: database connectors, role-based access, scheduled email reports, anomaly alerts, forecast models, data-quality profiling, and CI workflow. For production use, add authentication, data access controls, monitoring, and privacy review.

## License

MIT — see `LICENSE`.
