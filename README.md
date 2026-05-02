<div align="center">

# 📦 RetailOps Intelligence

**A zero-config logistics & retail analytics dashboard** — upload any CSV and instantly get **16 interactive charts**, KPI cards, geospatial maps, correlation matrices, and export tools.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://retailops-intelligence-fa8vgeqm4jpqltppwifakb.streamlit.app/)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

</div>

---

## ✨ Features

| Module | What You Get |
|--------|-------------|
| 📈 **Time-Series** | Line, area, range-selector, and subplot bar charts |
| 🥧 **Proportions** | Pie, donut, treemap & sunburst drilldown |
| 📊 **Statistics** | Box plot, violin, pivot heatmap, correlation matrix, histogram, ECDF |
| 🗺️ **Geospatial** | Marker, proportional circle, cluster, density heatmap & scatter-geo maps |

**Plus:**
- 🎛️ Smart column mapping via sidebar (date, metric, category, lat/lon)
- ⚡ KPI cards: Total, Mean, Max, Min, Row count, Category count
- 🔍 Live filters by category and date range
- ⬇️ One-click filtered CSV export
- 🌑 Full dark-mode UI with neon accent theme

---

## 🚀 Live Demo

👉 **[retailops-intelligence-fa8vgeqm4jpqltppwifakb.streamlit.app](https://retailops-intelligence-fa8vgeqm4jpqltppwifakb.streamlit.app/)**

---

## 🚀 Deploy on Streamlit Community Cloud (Free)

1. **Fork or clone** this repo

   ```bash
   git clone https://github.com/Arshitraj-123/retailops-intelligence.git
   cd retailops-intelligence
   ```

2. **Push to your GitHub** account

   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

3. **Go to [share.streamlit.io](https://share.streamlit.io)**
   - Sign in with GitHub
   - Click **New app**
   - Select your repo → branch `main` → main file `app.py`
   - Click **Deploy** 🎉

---

## 🛠️ Run Locally

**Prerequisites:** Python 3.9+

```bash
# 1. Clone the repo
git clone https://github.com/Arshitraj-123/retailops-intelligence.git
cd retailops-intelligence

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

Then open your browser at **http://localhost:8501**

---

## 📁 Project Structure

```
retailops-intelligence/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .python-version         # Forces Python 3.11 on Streamlit Cloud
└── README.md               # You are here
```

---

## 🗂️ CSV Format Guide

Your CSV can have **any column names** — you map them in the sidebar. Here's what each mapping does:

| Sidebar Field | Purpose | Example Column |
|--------------|---------|----------------|
| 📅 Date Column | X-axis for time-series charts | `order_date`, `created_at` |
| 📊 Primary Metric | Numeric values to aggregate | `sales`, `revenue`, `quantity` |
| 🏷️ Primary Category | Groups / segments | `region`, `product`, `status` |
| 🔖 Sub-Category | Second level for sunburst | `sub_category`, `city` |
| 🌐 Latitude | Geo coordinates | `lat`, `latitude` |
| 🌐 Longitude | Geo coordinates | `lon`, `longitude` |
| 🗺️ Geo Severity | Label shown on geo hover | `store_name`, `incident_type` |

---

## 🧰 Tech Stack

- **[Streamlit](https://streamlit.io)** — app framework
- **[Plotly](https://plotly.com/python/)** — interactive charts
- **[Folium](https://python-visualization.github.io/folium/)** — Leaflet.js maps
- **[streamlit-folium](https://github.com/randyzwitch/streamlit-folium)** — Folium ↔ Streamlit bridge
- **[Pandas](https://pandas.pydata.org/) & [NumPy](https://numpy.org/)** — data processing

---

## 📄 License

MIT — free to use, modify, and distribute.

---

<div align="center">
  Built with ❤️ using <b>Streamlit + Plotly + Folium</b>
</div>
