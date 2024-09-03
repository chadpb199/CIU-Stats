import sqlite3 as sql
import argparse as argp

con = sql.connect("ciu_stats.db")
cur = con.cursor()

parser = argp.ArgumentParser(
    prog="testing.py",
    description="""A script for adding or clearing test data to or from the 
        sqlite database for CIU-Stats"""
    )
    
parser.add_argument(
    "-c",
    "--clear",
    action="store_true",
    help="clear all data from the database"
    )
parser.add_argument(
    "-a",
    "--add",
    type=int,
    help="add N rows of test data to the database (default 5)",
    const=5,
    metavar="N",
    nargs="?",
    
    )

def clear_database():
    
    cur.execute("""DELETE FROM stats""")
    
    con.commit()
    
    print("All rows cleared from database.")
    
def add_testing_data(rows:int=5):
    
    try:
        last_row = int(cur.execute("""SELECT max(CRN) from stats"""
            ).fetchone()[0][0])
            
    except TypeError:
        last_row = -1
        
    new_row = last_row+1
        
    test_data = []
    cols = 8
    
    for r in range(new_row, new_row+rows):
        row = []
        for c in range(cols):
            row.append(f"{r}{c}")
            if len(row) == 8:
                test_data.append(row)
    
    cur.executemany("""
        INSERT INTO stats
        VALUES(?, ?, ?, ?, ?, ?, ?, ?)""",
        test_data
        )
        
    con.commit()
    
    print(f"{rows} rows added to database.")
        
        

if __name__ == "__main__":
    
    args = vars(parser.parse_args())
    
    if args["clear"]:
        clear_database()
    
    if args["add"] != None:
        add_testing_data(args["add"])
    
