import sqlite3 as sql
import argparse

con = sql.connect("ciu_stats.db")
cur = con.cursor()



def clear_database():
    
    cur.execute("""DELETE FROM stats""")
    
def add_testing_data(rows:int=5):
    
    test_data = []
    cols = 8
    
    for r in range(rows):
        for c in range(cols):            
            test_data.append(f"{r}{c}")
        
    test_data = [[i for i in test_data if i[0] == str(r)] for r in range(rows)]
    
    cur.executemany("""
        INSERT INTO stats
        VALUES(?, ?, ?, ?, ?, ?, ?, ?)""",
        test_data
        )
        
        

if __name__ == "__main__":
    clear_database()
    
    add_testing_data()
