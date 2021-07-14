import sqlite3
from sqlite3 import Error


def create_connection(db_file):

    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn
def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def insert_data(conn, datareadcv):

    sql = ''' INSERT INTO raw(id, datatime, sec_run, tile, tt, so_cuoc, so_an)
              VALUES(?,?,?,?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, datareadcv)
    conn.commit()
    return cur.lastrowid

def insert_analysis(conn, datareadcv):

    sql = ''' INSERT INTO analysis(id, tile_thap, tile_cao, tile_luc_thap, tile_luc_cao, aver,cci, dudoan, xxx)
              VALUES(?,?,?,?,?,?,?,?,?)'''

    cur = conn.cursor()
    cur.execute(sql, datareadcv)
    conn.commit()
    return cur.lastrowid
def select_all_raw(conn):

    cur = conn.cursor()
    cur.execute("SELECT * FROM raw")

    rows = cur.fetchall()

    for row in rows:
        print(row)

def select_all_analysis(conn):

    cur = conn.cursor()
    cur.execute("SELECT * FROM analysis")

    rows = cur.fetchall()

    for row in rows:
        print(row)


def delete_raw(conn, id):

    sql = 'DELETE FROM raw WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()


def delete_all_raw(conn):

    sql = 'DELETE FROM raw'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
def delete_all_analysis(conn):

    sql = 'DELETE FROM analysis'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

def main():

    database = "datamke.db"   
    sql_create_table = """ CREATE TABLE IF NOT EXISTS raw (
                                        id integer PRIMARY KEY,
                                        datatime text,
                                        sec_run integer,
                                        tile real,
                                        tt real,
                                        so_cuoc real,
                                        so_an real                                       
                                    ); """
    sql_create_analysis_table = """ CREATE TABLE IF NOT EXISTS analysis (
                                        id integer PRIMARY KEY,
                                        tile_thap real,
                                        tile_cao real,
                                        tile_luc_thap real,
                                        tile_luc_cao real,
                                        aver real,
                                        cci real,  
                                        dudoan integer,
                                        xxx interger                             
                                    ); """
    conn = create_connection(database)                            
    if conn is not None:
        create_table(conn, sql_create_table)
        create_table(conn, sql_create_analysis_table)
    else:
        print("Error! cannot create the database connection.")
    with conn:
        #select_all_raw(conn)  
        #select_all_analysis(conn) 
        #dataraw = (1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1, 1)
        #insert_analysis(conn, dataraw)

        x=0
        n=0
        cur = conn.cursor()
        cur.execute("SELECT id FROM raw WHERE id")
        lastrow = cur.fetchall()[-1][0]-120
        cur.execute("SELECT tile,sec_run,id FROM raw WHERE id > ? and sec_run = 31",(lastrow,))
        rows = cur.fetchall()
        row1=rows[0][2]
        row2=rows[1][2]
        print(row1,row2)
        cur.execute("SELECT tile FROM raw WHERE id between ? and ?",(row1,row2,))
        rows = cur.fetchall()
        for row in rows:
            print(row[0])
            x=x+row[0]
            n=n+1
        x=x/n
        print(n,x)

    ''' 
    for i in range(1,10):
        dataraw = (i,'10-11-12 10:10:10',50, 1.2223, 10, 1.2, 1.22)
        insert_data(conn, dataraw)
    '''  

    #delete_all_raw(conn)


    conn.close()
if __name__ == '__main__':
    main()

