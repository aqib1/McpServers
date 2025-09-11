from mcp.server.fastmcp import FastMCP
import sqlite3
import os
from typing import Any, List, Dict, Optional

mcp = FastMCP("SQLITE Server")
DB_PATH = '/Users/aqibjaved/VsCode/db/'

def get_db_connection(db_name: str):
    """Create a connection to the SQLite database."""
    conn = sqlite3.connect(f'{DB_PATH}{db_name}.db')
    conn.row_factory = sqlite3.Row
    return conn

def dict_form_row(row):
    """Convert a SQLite row to a dictionary."""
    return dict(row) if row else None

def dict_form_rows(rows):
    """Convert a list of SQLite rows to a list of dictionaries."""
    return [dict_form_row(row) for row in rows]

@mcp.tool()
def get_countries(
        name: Optional[str] = None,
        iso2: Optional[str] = None,
        iso3: Optional[str] = None,
        capital: Optional[str] = None,
        currency: Optional[str] = None,
        limit: int = 100,
) -> List[Dict[str, Any]]:
    """
    Get countries with optional filters. Filter parameters are optional and if not provided, 
    then all countries will be returned.

    Args:
        name (str, optional): Filter by country name.
        iso2 (str, optional): Filter by ISO2 code.
        iso3 (str, optional): Filter by ISO3 code.
        capital (str, optional): Filter by capital city.
        currency (str, optional): Filter by currency code.
        limit (int, optional): Maximum number of results to return. Default is 100.

    Returns:
        List[Dict[str, Any]]: List of countries matching the filters.
    """
    conn = get_db_connection('world')
    query = "SELECT * FROM countries WHERE 1=1"
    params = []
    if name:
        query += " AND name LIKE ?"
        params.append(f"%{name}%")
    if iso2:
        query += " AND iso2 = ?"
        params.append(iso2)
    if iso3:
        query += " AND iso3 = ?"
        params.append(iso3)
    if capital:
        query += " AND capital LIKE ?"
        params.append(f"%{capital}%")
    if currency:
        query += " AND currency = ?"
        params.append(currency)
    query += " LIMIT ?"
    params.append(limit)
    cursor = conn.execute(query, params)
    results = dict_form_rows(cursor.fetchall())
    conn.close()
    return results

@mcp.tool()
def get_top_chatters():
    """Retrieve the top chatters sorted by number of messages."""
    conn = get_db_connection('community')
    cursor = conn.cursor()

    cursor.execute("SELECT name, messages FROM chatters ORDER BY messages DESC")
    results = cursor.fetchall()
    conn.close()

    chatters = [{"name": name, "messages": messages} for name, messages in results]
    return results

@mcp.tool()
def search_countries_by_name(name: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Search countries by name for (partial matches allowed) with a limit on the number of results."""
    conn = get_db_connection('world')

    if name:
        query = "SELECT * FROM countries WHERE name LIKE ? LIMIT ?"
        params = (f"%{name}%", limit)
    else:
        query = "SELECT * FROM countries LIMIT ?"
        params = (limit,)

    cursor = conn.execute(query, params)
    results = dict_form_rows(cursor.fetchall())
    conn.close()
    return results

@mcp.tool()
def get_country_by_iso(iso_code: str) -> Optional[Dict[str, Any]]:
    """Get a country by its ISO2 or ISO3 code."""
    conn = get_db_connection('world')
    query = "SELECT * FROM countries WHERE iso2 = ? OR iso3 = ?"
    params = (iso_code, iso_code)
    cursor = conn.execute(query, params)
    row = cursor.fetchone()
    conn.close()
    return dict_form_row(row)

@mcp.tool()
def get_country_by_region(region: str) -> List[Dict[str, Any]]:
    """Get countries by region."""
    conn = get_db_connection('world')
    query = "SELECT * FROM countries WHERE region = ?"
    params = (region,)
    cursor = conn.execute(query, params)
    results = dict_form_rows(cursor.fetchall())
    conn.close()
    return results

@mcp.tool()
def get_counrty_by_currency(currency: str) -> List[Dict[str, Any]]:
    """Get countries by currency."""
    conn = get_db_connection('world')
    query = "SELECT * FROM countries WHERE currency = ?"
    params = (currency,)
    cursor = conn.execute(query, params)
    results = dict_form_rows(cursor.fetchall())
    conn.close()
    return results

@mcp.tool()
def get_cities(name: str = "", country_code: str = "", limit: int = 10) -> List[Dict[str, Any]]:
    """Get cities by name and/or country code with a limit on the number of results."""
    conn = get_db_connection('world')
    query = "SELECT * FROM cities WHERE 1=1"
    params = []
    if name:
        query += " AND name LIKE ?"
        params.append(f"%{name}%")
    if country_code:
        query += " AND country_code = ?"
        params.append(country_code)
    query += " ORDER BY name LIMIT ?"
    params.append(limit)
    cursor = conn.execute(query, params)
    results = dict_form_rows(cursor.fetchall())
    conn.close()
    return results

@mcp.tool()
def get_cities_in_country(country_code: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Get cities in a specific country by country code with a limit on the number of results."""
    conn = get_db_connection('world')
    query = "SELECT * FROM cities WHERE country_code = ? ORDER BY name LIMIT ?"
    params = (country_code, limit)
    cursor = conn.execute(query, params)
    results = dict_form_rows(cursor.fetchall())
    conn.close()
    return results

@mcp.tool()
def get_states_in_country(country_code: str) -> List[Dict[str, Any]]:
    """Get states/provinces in a specific country by country code."""
    conn = get_db_connection('world')
    query = "SELECT * FROM states WHERE country_code = ? ORDER BY name"
    params = (country_code,)
    cursor = conn.execute(query, params)
    results = dict_form_rows(cursor.fetchall())
    conn.close()
    return results

if __name__ == "__main__":
    mcp.run()