# ** Exploring AMD's Stock Surge Using Power BI** 

## **Overview**

This project examines the relationship between **AMD’s stock performance** and key macroeconomic factors, with a focus on the **Federal Reserve’s interest rate decisions** and **Earnings Per Share (EPS)** trends. Data was gathered from the **Alpha Vantage API** and visualized in **Power BI** to reveal correlations between AMD’s stock price movements and changes in the **federal funds rate**.

---

## **📊 Project Workflow**

### 1. **Creating the SQLite Database and Tables**

A **SQLite database** was created using Python’s `sqlite3` library to store both AMD's weekly stock price data and the Federal Reserve's interest rate data. This provided a structured way to efficiently manage and retrieve the data for analysis.

- A table named `weekly_adjusted_stocks` was established to store AMD’s weekly stock data, which includes columns for `open`, `high`, `low`, `close`, `volume`, and `date`.
- A second table, `federal_funds_rate`, was created to store the Federal Reserve's interest rate data, with columns for `rate` and `date`.
- Other tables were also created, a few more were used in the visuals depicted in PowerBI.

#### **Fetching Data:**
- **Weekly stock prices** for AMD were retrieved and inserted into the `weekly_adjusted_stocks` table. Each record was associated with a unique date to prevent duplicates.
- Similarly, data on the **federal funds rate** was fetched and inserted into the `federal_funds_rate` table, ensuring that each rate matched the corresponding time period.

---

### 2. **Connecting SQLite Database to Power BI via ODBC**

The **SQLite database** was connected to Power BI using an **ODBC (Open Database Connectivity)** connector. An ODBC data source was set up for the SQLite database, allowing Power BI to directly access and retrieve the stored data for visualization.

- This connection enabled Power BI to query and pull data from the `stocks.db` database, linking the stock price and federal funds rate data for analysis.

---

### 3. **Creating a Date Table in Power BI**

To ensure consistency across all visuals, a **Date Table** was generated in Power BI. This allowed the proper synchronization of time-based data, such as stock prices and interest rates, across the various visualizations.

- Relationships between the **Date Table** and the `weekly_adjusted_stocks`, `federal_funds_rate`, etc. were established, aligning the time-series data across different datasets.
- This approach helped create accurate representations of **AMD's stock performance** over time in relation to interest rate changes.

---

## **🔍 Key Insights**

- **Interest Rate Correlation**: The analysis found a correlation between AMD’s stock performance and changes in the **federal funds rate**. Stock price increases were observed during rate cuts, while rate hikes led to significant declines.
  
- **Resilience in Stock Performance**: Despite the volatility caused by rate changes, AMD demonstrated resilience, achieving a new **all-time high in 2024** due to market expectations of future rate cuts and strong earnings.

---
