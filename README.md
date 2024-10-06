## **📈 Exploring AMD's Stock Surge (2016 - Present)** 

## **Overview**

This project examines the relationship between **AMD’s stock performance** and key macroeconomic factors, with a focus on the **Federal Reserve’s interest rate** and **Earnings Per Share (EPS)** trends. Data was gathered using a **Alpha Vantage API Key** and visualized in **Power BI** to reveal correlations between AMD’s stock price movements and changes in the **federal funds rate**.

---

## **📊 Project Workflow**

### 1. **Creating the SQLite Database and Tables**

A **SQLite database** was created using Python’s `sqlite3` library to store AMD's weekly stock price data, the Federal Reserve's interest rate data, etc. This provided a structured way to efficiently manage and retrieve the data for analysis.

- A table named `weekly_adjusted_stocks` was established to store AMD’s weekly stock data, which includes columns for `open`, `high`, `low`, `close`, `volume`, and `date`.
- A second table, `federal_funds_rate`, was created to store the Federal Reserve's interest rate data, with columns for `rate` and `date`.
- Other tables were also created, a few more were used in the visuals depicted in PowerBI.

### 2. **Data Fetching and Insertion**

The project uses a two-step method to **retrieve financial data** from an external API (Alpha Vantage) and **insert it** into a local SQLite database for further analysis and visualization.

#### **Fetching Data**:
- **API Request**: Data such as stock prices or economic indicators are retrieved using the **Alpha Vantage API**. The function `fetch_financial_data(function_name)` is responsible for this process.
   - The function sends an API request with the specific `function_name` (e.g., `'EARNINGS'`, `'TIME_SERIES_WEEKLY'`) and the API key.
   - It validates the API response by checking the HTTP status code. If the request is successful, the data is returned in JSON format.
     
#### **Inserting Data**:
- After successfully retrieving the data, it is inserted into an **SQLite database** (`stocks.db`) using the `insert_eps_data()` or similar insertion functions.
   - These functions open a connection to the database and execute **SQL queries** to store the data in structured tables.
   - The data is inserted into the appropriate table, such as `earnings`, ensuring that no duplicate entries are created thanks to the `INSERT OR IGNORE` SQL command.

---

### 3. **Connecting SQLite Database to Power BI via ODBC**

The **SQLite database** was connected to Power BI using an **ODBC (Open Database Connectivity)** connector. An ODBC data source was set up for the SQLite database, allowing Power BI to directly access and retrieve the stored data for visualization.

- This connection enabled Power BI to query and pull data from the `stocks.db` database.
---

### 4. **Creating a Date Table in Power BI**

To ensure consistency across all visuals, a **Date Table** was generated in Power BI. This allowed the proper synchronization of time-based data, such as stock prices and interest rates, across the various visualizations.

- Relationships between the **Date Table** and the `weekly_adjusted_stocks`, `federal_funds_rate`, etc. were established, aligning the time-series data across different datasets.
- This approach helped create accurate representations of **AMD's stock performance** over time in relation to interest rate changes.

### 5. **Adding Visuals in Power BI**

Several visuals were developed in **Power BI** to illustrate the relationship between AMD's stock performance (2016 - present) and key economic indicators, offering deeper insights into market trends:

- **Line and Column Chart (Stock Price vs. Federal Funds Rate):**
   - This chart tracked the relationship between **stock price fluctuations** and **interest rate adjustments**, highlighting notable correlations during **rate cuts and hikes**.

- **Line and Column Chart (Stock Price vs. Earnings Per Share):**
   - This visual underscored how **corporate earnings**, particularly changes in **EPS**, influenced stock prices over the same period.

- **100% Stacked Column Chart (Total Assets vs. Liabilities):**
   - This chart provided a clear visualization of **AMD’s evolving financial structure**, highlighting a **decrease in liabilities relative to assets**, signaling improved financial stability.

- **Line Chart (Logarithmic Scale Stock Price vs. Linear Scale Stock Price):**
   - The **log scale** helped normalize large price jumps, allowing for a clearer interpretation of **long-term growth trends** without distortion caused by short-term volatility.

These visuals offered a comprehensive view of how **macroeconomic shifts**, **company earnings**, and **financial health indicators** influenced AMD’s stock trajectory, providing valuable insights into its performance over time.

---

## **🔍 Key Insights**

- **Interest Rate Correlation**: The analysis found a correlation between AMD’s stock performance and changes in the **federal funds rate**. Stock price increases were observed during rate cuts, while rate hikes led to significant declines.
  
- **Resilience in Stock Performance**: Despite the volatility caused by rate changes, AMD demonstrated resilience, achieving a new **all-time high in 2024** due to market expectations of future rate cuts and strong earnings.

## **📄 Project Files**

- [Data Retrieval Script](AMD_Stock_Data.py): Python script that pulls data using Alpha Vantage's API and stores it in an SQLite database.
- [Power BI Report](AMD_Stock_Analysis.pbix): Power BI report that visualizes AMD's stock performance and interest rate data.
- [Report PDF](AMD_Stock_Analysis.pdf): Power BI report downloadable as a pdf.

---
