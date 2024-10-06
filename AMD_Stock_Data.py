import requests
import sqlite3
import pandas as pd
from datetime import datetime

api_key = 'K59E9GVKI4WNXPO9'
api_url = 'https://www.alphavantage.co/query'

def create_tables():
    with sqlite3.connect("stocks.db") as conn:
        cursor = conn.cursor()

        # Existing tables
        create_inflation_table_query = """
        CREATE TABLE IF NOT EXISTS inflation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            cpi REAL,
            UNIQUE(date)
        );
        """
        cursor.execute(create_inflation_table_query)

        create_federal_funds_rate_query = """
        CREATE TABLE IF NOT EXISTS federal_funds_rate (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            rate REAL,
            UNIQUE(date)
        );
        """
        cursor.execute(create_federal_funds_rate_query)

        create_unemployment_rate_query = """
        CREATE TABLE IF NOT EXISTS unemployment_rate (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            rate REAL,
            UNIQUE(date)
        );
        """
        cursor.execute(create_unemployment_rate_query)

        create_real_gdp_query = """
        CREATE TABLE IF NOT EXISTS real_gdp (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            gdp REAL,
            UNIQUE(date)
        );
        """
        cursor.execute(create_real_gdp_query)

        create_stock_table_query = """
        CREATE TABLE IF NOT EXISTS weekly_adjusted_stocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT,
            date TEXT,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume INTEGER,
            UNIQUE(symbol, date)
        );
        """
        cursor.execute(create_stock_table_query)

        # New tables for EPS, Balance Sheet, and Income Statement
        create_eps_table_query = """
        CREATE TABLE IF NOT EXISTS earnings_per_share (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            eps REAL,
            UNIQUE(date)
        );
        """
        cursor.execute(create_eps_table_query)

        create_balance_sheet_table_query = """
        CREATE TABLE IF NOT EXISTS balance_sheet (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            assets REAL,
            liabilities REAL,
            UNIQUE(date)
        );
        """
        cursor.execute(create_balance_sheet_table_query)

        create_income_statement_table_query = """
        CREATE TABLE IF NOT EXISTS income_statement (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            revenue REAL,
            expenses REAL,
            UNIQUE(date)
        );
        """
        cursor.execute(create_income_statement_table_query)

        conn.commit()

def fetch_financial_data(function_name):
    params = {
        'function': function_name,
        'apikey': api_key
    }
    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching {function_name} data: {response.status_code}")
        return None

def insert_inflation_data(data):
    inflation_data = data.get('data', data.get('data_series', []))
    with sqlite3.connect("stocks.db") as conn:
        cursor = conn.cursor()
        insert_query = "INSERT OR IGNORE INTO inflation (date, cpi) VALUES (?, ?)"
        for row in inflation_data:
            cursor.execute(insert_query, (row['date'], float(row['value'])))
        conn.commit()

def insert_federal_funds_rate_data(data):
    fed_funds_data = data.get('data', data.get('data_series', []))
    with sqlite3.connect("stocks.db") as conn:
        cursor = conn.cursor()
        insert_query = "INSERT OR IGNORE INTO federal_funds_rate (date, rate) VALUES (?, ?)"
        for row in fed_funds_data:
            cursor.execute(insert_query, (row['date'], float(row['value'])))
        conn.commit()

def insert_unemployment_rate_data(data):
    unemployment_data = data.get('data', data.get('data_series', []))
    with sqlite3.connect("stocks.db") as conn:
        cursor = conn.cursor()
        insert_query = "INSERT OR IGNORE INTO unemployment_rate (date, rate) VALUES (?, ?)"
        for row in unemployment_data:
            cursor.execute(insert_query, (row['date'], float(row['value'])))
        conn.commit()

def insert_real_gdp_data(data):
    gdp_data = data.get('data', data.get('data_series', []))
    with sqlite3.connect("stocks.db") as conn:
        cursor = conn.cursor()
        insert_query = "INSERT OR IGNORE INTO real_gdp (date, gdp) VALUES (?, ?)"
        for row in gdp_data:
            cursor.execute(insert_query, (row['date'], float(row['value'])))
        conn.commit()

def insert_eps_data(data):
    eps_data = data.get('data', data.get('data_series', []))
    with sqlite3.connect("stocks.db") as conn:
        cursor = conn.cursor()
        insert_query = "INSERT OR IGNORE INTO earnings_per_share (date, eps) VALUES (?, ?)"
        for row in eps_data:
            cursor.execute(insert_query, (row['date'], float(row['value'])))
        conn.commit()

def insert_balance_sheet_data(data):
    balance_data = data.get('data', data.get('data_series', []))
    with sqlite3.connect("stocks.db") as conn:
        cursor = conn.cursor()
        insert_query = "INSERT OR IGNORE INTO balance_sheet (date, assets, liabilities) VALUES (?, ?, ?)"
        for row in balance_data:
            cursor.execute(insert_query, (
                row['date'], 
                float(row['assets']), 
                float(row['liabilities'])
            ))
        conn.commit()

def insert_income_statement_data(data):
    income_data = data.get('data', data.get('data_series', []))
    with sqlite3.connect("stocks.db") as conn:
        cursor = conn.cursor()
        insert_query = "INSERT OR IGNORE INTO income_statement (date, revenue, expenses) VALUES (?, ?, ?)"
        for row in income_data:
            cursor.execute(insert_query, (
                row['date'], 
                float(row['revenue']), 
                float(row['expenses'])
            ))
        conn.commit()

def fetch_weekly_adjusted_stock_data(symbol):
    params = {
        'function': 'TIME_SERIES_WEEKLY',
        'symbol': symbol,
        'apikey': api_key
    }
    response = requests.get(api_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if 'Weekly Time Series' in data:
            return data
        else:
            print(f"Error: No 'Weekly Time Series' data found for {symbol}")
            return None
    else:
        print(f"Error fetching stock data: {response.status_code} - {response.text}")
        return None

def insert_stock_data_to_db(symbol, data):
    with sqlite3.connect("stocks.db") as conn:
        cursor = conn.cursor()

        insert_query = """
        INSERT OR REPLACE INTO weekly_adjusted_stocks (symbol, date, open, high, low, close, volume)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        time_series = data.get('Weekly Time Series', {})
        
        for date, metrics in time_series.items():
            cursor.execute(insert_query, (
                symbol,
                datetime.strptime(date, '%Y-%m-%d').date(),
                float(metrics.get('1. open', 0)),
                float(metrics.get('2. high', 0)),
                float(metrics.get('3. low', 0)),
                float(metrics.get('4. close', 0)),
                int(metrics.get('5. volume', 0))
            ))

        conn.commit()
        print(f"Stock data for {symbol} inserted or updated successfully!")

def main():
    symbol = 'AMD'

    create_tables()

    inflation_data = fetch_financial_data('CPI')
    if inflation_data:
        insert_inflation_data(inflation_data)

    fed_funds_data = fetch_financial_data('FEDERAL_FUNDS_RATE')
    if fed_funds_data:
        insert_federal_funds_rate_data(fed_funds_data)

    unemployment_data = fetch_financial_data('UNEMPLOYMENT')
    if unemployment_data:
        insert_unemployment_rate_data(unemployment_data)

    gdp_data = fetch_financial_data('REAL_GDP')
    if gdp_data:
        insert_real_gdp_data(gdp_data)

    stock_data = fetch_weekly_adjusted_stock_data(symbol)
    if stock_data:
        insert_stock_data_to_db(symbol, stock_data)

    eps_data = fetch_financial_data('EARNINGS')
    if eps_data:
        insert_eps_data(eps_data)

    balance_sheet_data = fetch_financial_data('BALANCE_SHEET')
    if balance_sheet_data:
        insert_balance_sheet_data(balance_sheet_data)

    income_statement_data = fetch_financial_data('INCOME_STATEMENT')
    if income_statement_data:
        insert_income_statement_data(income_statement_data)

if __name__ == "__main__":
    main()
