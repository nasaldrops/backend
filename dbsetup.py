import os
from dotenv import load_dotenv
import pyodbc

load_dotenv()

conn_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={os.getenv('DB_SERVER')};DATABASE={os.getenv('DB_DATABASE')};UID={os.getenv('DB_USERNAME')};PWD={os.getenv('DB_PASSWORD')}"

create_projects_table = """
CREATE TABLE Projects (
    project_id INT PRIMARY KEY,
    title NVARCHAR(100),
    description TEXT,
    status_id INT,
    researcher_id INT
);
"""

# Connect to the database
with pyodbc.connect(conn_string) as conn:
    cursor = conn.cursor()
    cursor.execute(create_projects_table)
    print("Table Created")
