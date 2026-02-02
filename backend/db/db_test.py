import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent      
PROJECT_DIR = BASE_DIR.parent.parent           
db_path = PROJECT_DIR / "database" / "insurance.db"

print("DB path:", db_path)
print("DB exists:", db_path.exists()) 


try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    if tables:
        print("Tables in the database:")
        for table in tables:
            print("-", table[0])
    else:
        print("No tables found in the database.")
    
    conn.close()
except sqlite3.OperationalError as e:
    print("Error opening database:", e)
