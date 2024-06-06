import pyodbc

conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=127.0.0.1,1433;"
    "DATABASE=RPA;"
    "UID=sa;"
    "PWD=1Secure*Password1"
)

try:
    with pyodbc.connect(conn_str, timeout=5) as conn:
        print("Connection successful!")
except Exception as e:
    print(f"Connection failed: {e}")