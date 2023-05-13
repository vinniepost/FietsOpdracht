import sqlite3
from sqlite3 import Error
import json

def create_connection(bd_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(bd_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    return conn

def select_all_tasks(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM Fietsen")
    rows = cur.fetchall()

    for row in rows:
        print(row)

def select_task_by_priority(conn, priority):
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE priority=?", (priority,))
    rows = cur.fetchall()

    for row in rows:
        print(row)

def Add_DB_Entree(conn, table, values):
    cur = conn.cursor()

    print(values)
    cur.execute("INSERT INTO " + table + " VALUES " + values)
    conn.commit()

def Add_DB_Bulk(conn, table, values):
    for value in values:
        Add_DB_Entree(conn, table, value)

def main():   
    database = r"data/AplicatieDB.sqlite"
    # create a database connection
    conn = create_connection(database)
    with conn:   
        dataList = []
        with open("data/fietsen.json", "r") as data_file:
            dataDict = json.load(data_file)
            dataList = []
            for data in dataDict:
                dataList.append('('  + str(dataDict[data]["id"]) +',' + "'"+dataDict[data]["status"] +"'"+ ',' + "'"+dataDict[data]["Lokatie"] +"'"+ ')')        
        Add_DB_Bulk(conn, "Fietsen", dataList)
        #Add_DB_Entree(conn, "Fietsen", "(1, 'test',1,1)")

if __name__ == '__main__':
    main()
