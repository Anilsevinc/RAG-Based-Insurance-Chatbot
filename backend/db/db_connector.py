# backend/db/db_connector.py
import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent    
PROJECT_DIR = BASE_DIR.parent.parent            
db_path = PROJECT_DIR / "database" / "insurance.db"

def connect_to_db(db_path=db_path):

    #Connect to the SQLite database
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    return conn, cursor

def get_faq_data(db_path=db_path):
    
    # Fetch all data from the FAQ table
    conn, cursor = connect_to_db(str(db_path))
    query = "SELECT question, answer FROM FAQ"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
