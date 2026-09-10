# ONS Thermal Power Generation Data Pipeline ⚡📊

## Project Overview
This project delivers an automated **Data Pipeline (ETL)** built in Python to monitor daily electricity generation in Brazil. It automates the extraction of **Daily Thermal Production Reports per Power Plant** from the official portal of the **ONS (Operador Nacional do Sistema Elétrico)**.

The script programmatically iterates through a user-defined month and year using the `datetime` library, bypasses manual download constraints via `requests`, cleans the raw tables, and leverages **Pandas** to consolidate daily metrics into a structured, multi-sheet monthly executive summary in Excel (`.xlsx`) using the `openpyxl` engine.

### Why this matters for the Energy & Gas Sector
In the Brazilian energy matrix, thermal power dispatch is the primary driver of natural gas consumption (thermoelectric dispatch). Automating the ingestion of ONS thermal generation data allows energy analysts, regulatory specialists, and trading desks to track real-time gas demand fluctuations, evaluate plant operation status, and forecast fuel commodity pricing changes with precision.

---

## 🛠️ Tech Stack & Libraries
- **Language:** Python 3.x
- **Data Ingestion:** `Requests` & `Datetime` (Iterative URL Ingestion)
- **Data Manipulation & Transformation:** `Pandas` (Pivot Tables & Data Cleaning)
- **Data Output (Loading):** `OpenPyXL` (Multi-sheet Excel generation)

---

## ⚙️ Data Pipeline Architecture

1. **Extraction (Ingestion):** The pipeline programmatically checks the ONS directory structure, handles potential `404 Not Found` errors for non-operating days, and downloads the raw daily files into a local `data/` directory.
2. **Transformation (Processing):**
   - Normalizes raw data structures by skipping ONS metadata headers (`header=20`).
   - Cleans missing values (`dropna`) and removes whitespace anomalies from plant names (`str.strip()`).
   - Transforms long daily rows into a structured wide matrix (**Pivot Table**) tracking daily generation (`MWmed`) per asset across the entire month.
   - Filters and reindexes a customized list of strategic thermal assets for regional gas monitoring (e.g., *UTE Mauá 3, Tambaqui, Pirarucu, Tucunaré*).
3. **Loading (Output):** Generates an optimized Excel workbook containing three relational layers: `Base_Completa`, `Resumo_Todas_Usinas`, and `Usinas_Selecionadas`.

---

## 📂 How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/OtavioMDS3141/ons-thermal-generation-automation
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the pipeline:
   ```bash
   python src/ons_generation_pipeline.py
   ```

---
*Developed as part of my advanced portfolio in Energy Market Regulation & Business Analytics.*
