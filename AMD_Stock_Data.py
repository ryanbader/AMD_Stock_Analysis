import sqlite3
from datetime import datetime

import pandas as pd
import requests
from pydantic import BaseModel

api_key = "SL4HRANNVQRZ3VUZ"
api_url = "https://www.alphavantage.co/query"


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


class BasicData(BaseModel):
    date: datetime
    value: float


class IncomeData(BaseModel):
    date: datetime
    revenue: float
    expenses: float


class BalanceSheetData(BaseModel):
    date: datetime
    assets: float
    liabilities: float


class StockData(BaseModel):
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int


class FinancialData(BaseModel):
    data: list[BasicData] | list[IncomeData] | list[BalanceSheetData]


class SeriesData(BaseModel):
    data_series: list[StockData]


def fetch_financial_data(function_name):
    params = {"function": function_name, "apikey": api_key}
    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        data = response.json()
        print(data)
        fd = FinancialData.model_validate(data)
        return fd
    else:
        print(f"Error fetching {function_name} data: {response.status_code}")
        return None


def fetch_stock_data(symbol):
    params = {"symbol": symbol, "function": "TIME_SERIES_WEEKLY", "apikey": api_key}
    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        data = response.json()
        sd = SeriesData.model_validate(data)
        return sd
    else:
        print(f"Error fetching {symbol} data: {response.status_code}")
        return None


def insert_data(query: str, data: list[tuple]):
    with sqlite3.connect("stocks.db") as conn:
        cursor = conn.cursor()
        cursor.executemany(query, data)
        conn.commit()


def insert_federal_funds_rate_data(fed_funds_data: list[BasicData]):
    data = [(i.date, i.value) for i in fed_funds_data]
    insert_data(
        "INSERT OR REPLACE INTO federal_funds_rate (date, rate) VALUES (?, ?)", data
    )


def insert_unemployment_rate_data(unemployment_data: list[BasicData]):
    data = [(i.date, i.value) for i in unemployment_data]
    insert_data = (
        "INSERT OR REPLACE INTO unemployment_rate (date, rate) VALUES (?, ?)",
        data,
    )


def insert_real_gdp_data(real_gdp_data: list[BasicData]):
    data = [(i.date, i.value) for i in real_gdp_data]
    insert_data("INSERT OR REPLACE INTO real_gdp (date, gdp) VALUES (?, ?)", data)


def insert_eps_data(eps_data: list[BasicData]):
    data = [(i.date, i.value) for i in eps_data]
    insert_data(
        "INSERT OR REPLACE INTO earnings_per_share (date, eps) VALUES (?, ?)", data
    )


def insert_balance_sheet_data(balance_sheet_data: list[BalanceSheetData]):
    data = [(i.date, i.assets, i.liabilities) for i in balance_sheet_data]
    insert_data(
        "INSERT OR REPLACE INTO balance_sheet (date, assets, liabilities) VALUES (?, ?, ?)",
        data,
    )


def insert_income_statement_data(income_data: list[IncomeData]):
    data = [(i.date, i.revenue, i.expenses) for i in income_data]
    insert_data(
        "INSERT OR REPLACE INTO income_statement (date, revenue, expenses) VALUES (?, ?, ?)",
        data,
    )


def insert_inflation_data(inflation_data: list[BasicData]):
    data = [(i.date, i.value) for i in inflation_data]
    insert_data("INSERT OR REPLACE INTO inflation (date, cpi) VALUES (?, ?)", data)


def insert_stock_data_to_db(stock_data: list[StockData]):
    data = [(i.date, i.open, i.high, i.low, i.close, i.volume) for i in stock_data]
    insert_data(
        """INSERT OR REPLACE INTO weekly_adjusted_stocks (date, open, high, low, close, volume) VALUES (?, ?, ?, ?, ?, ?, ?)""",
        data,
    )


def main():

    create_tables()

    symbol = "AMD"

    inflation_data = fetch_financial_data("CPI")
    if inflation_data:
        insert_inflation_data(inflation_data.data)

    fed_funds_data = fetch_financial_data("FEDERAL_FUNDS_RATE")
    if fed_funds_data:
        insert_federal_funds_rate_data(fed_funds_data.data)

    unemployment_data = fetch_financial_data("UNEMPLOYMENT")
    if unemployment_data:
        insert_unemployment_rate_data(unemployment_data.data)

    gdp_data = fetch_financial_data("REAL_GDP")
    if gdp_data:
        insert_real_gdp_data(gdp_data.data)

    stock_data = fetch_financial_data(symbol)
    if stock_data:
        insert_stock_data_to_db(stock_data.data_series)

    eps_data = fetch_financial_data("EARNINGS")
    if eps_data:
        insert_eps_data(eps_data.data)

    balance_sheet_data = fetch_financial_data("BALANCE_SHEET")
    if balance_sheet_data:
        insert_balance_sheet_data(balance_sheet_data.data)

    income_statement_data = fetch_financial_data("INCOME_STATEMENT")
    if income_statement_data:
        insert_income_statement_data(income_statement_data.data)


if __name__ == "__main__":
    main()
