import sqlite3
from sqlite3 import Error
import xlrd
import time
from time import strftime
import os
from datetime import datetime

tm = time.localtime()
tmStmp = "{}{}{}".format(tm.tm_mday, tm.tm_mon, tm.tm_year)


class DatabaseSQLite:
    def __init__(self):
        # db_dir
        self.db_dir = "vietcuppos/local_database/"
        if not os.path.exists(self.db_dir):
            os.makedirs(self.db_dir)

        # .db file
        self.db = "VietCupPOS.db"

    def fetchLastRow(self, table_name, conn):
        try:
            rw = conn.execute(
                'select * from {}'.format(table_name)).fetchall()[-1]
            return rw
        except Error as e:
            # pass
            print(e)
            return None
        finally:
            if conn:
                conn.close()

    # Insert into database
    def insert_into_database(self, tableName, conn, data):

        if conn is not None:
            try:
                c = conn.execute("select * from {}".format(tableName))
                fields = tuple([des[0] for des in c.description][:])
                # print(fields)
                print("DATA : {}".format(data))
                if "id" in fields:
                    fields = tuple(list(fields)[1:])
                print("FIELDS : {}".format(fields))
                cur = conn.cursor()
                cur.execute("""
					INSERT INTO {} {} VALUES {}
					""".format(tableName, fields, data)
                )
                cur.close()
                conn.commit()
                print("Inserted")
                return self.fetchLastRow(tableName, conn)
            except Error as e:
                # pass
                print(e)
            finally:
                if conn:
                    conn.close()
        return None

    # Update Database
    def update_database(self, tableName, conn, fields, field_vals, ref, index):
        if conn is not None:
            try:
                cur = conn.cursor()
                if not isinstance(fields, tuple) and not isinstance(fields, list):
                    fields = list([fields])
                    field_vals = list([field_vals])

                for field, field_val in zip(fields, field_vals):
                    # print(field,field_val)
                    cur.execute(
                        """
							UPDATE {}
							SET {}= ? WHERE {}= ?
							""".format(
                            tableName, field, ref
                        ),
                        (field_val, index),
                    )
                conn.commit()
                return True
            except Exception as e:
                pass
                # print("Error in updating data: {}".format(e))
        return None

    # Delete from Database
    def delete_from_database(self, tableName, conn, condition):
        if conn is not None:
            try:
                cur = conn.cursor()
                # just to track if deletion was successful
                count = len(
                    cur.execute(
                        """
						SELECT * FROM {} WHERE {}
						""".format(
                            tableName, condition
                        )
                    ).fetchall()
                )
                if not count:
                    return False
                cur.execute(
                    """
						DELETE FROM {} WHERE {}
						""".format(
                        tableName, condition
                    )
                )
                conn.commit()
                return True
            except Error as e:
                pass
                # print("Error in deleting data: {}".format(e))
        return False

    # Search in the database
    def search_from_database(self, tableName, conn, prop, value, order_by="-id"):
        if conn is not None:
            try:
                cur = conn.cursor()
                # print("cur: {}".format(cur))
                filtered_list = cur.execute(
                    """
							SELECT * FROM {} WHERE {} LIKE ? ORDER BY {};
						""".format(
                        tableName, prop, order_by
                    ),
                    (str(value) + "%",),
                ).fetchall()
                return filtered_list
            except Error as e:
                pass
                # print("Error in searching: {}".format(e))

        return None

    def search_from_database_many(self, tableName, conn, condition):
        if conn is not None:
            try:
                cur = conn.cursor()
                filtered_list = cur.execute(
                    """
						SELECT * FROM {} WHERE {}
						""".format(
                        tableName, condition
                    )
                ).fetchall()
                return filtered_list
            except Error as e:
                pass
                # print("Error in deleting data: {}".format(e))
        return None

    # connect database
    def connect_database(self):
        conn = None
        try:
            conn = sqlite3.connect(
                self.db_dir + self.db, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
            print("DB connected")
        except Error:
            pass
            #print("Error in database: {}".format(e))
        finally:
            return conn

    # create table
    def create_table(self, table, conn):
        if conn is not None:
            try:
                cur = conn.cursor()
                cur.execute(table)
                cur.close()
                conn.commit()
                print("Table created")
            except Error:
                pass
            finally:
                conn.close()

    def delete_table(self, db_file, table_name):
        conn = self.connect_database(db_file)
        if conn is not None:
            cur = conn.cursor()
            try:
                cur.execute("DROP TABLE {}".format(table_name))
                conn.commit()
                conn.close()
                return True
            except:
                return False

    def findTables(self):
        conn = self.connect_database()
        if conn is not None:
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
            return [each[0] for each in cur.fetchall()]
        # conn.close()

    def readFile(self, db_file, table, tableName, file_name, **kwargs):

        table = table.format(tableName)
        try:
            wb = xlrd.open_workbook(file_name)
            sheet = wb.sheet_by_index(0)
            rows = sheet.nrows

            conn = self.connect_database(db_file)

            if conn is not None:
                self.create_table(table, conn)

                for i in range(1, rows):
                    data = (
                        sheet.cell_value(i, 1),
                        sheet.cell_value(i, 2),
                        kwargs["course"],
                        kwargs["stream"],
                        kwargs["fromYear"] + "-" + kwargs["toYear"],
                        kwargs["fee"],
                        sheet.cell_value(i, 3),
                    )

                    self.insert_into_database(tableName, conn, data)
                conn.close()
                return True

            return False
        except:
            return False

    def addData(self, db_file, table, tableName, data):

        table = table.format(tableName)
        conn = self.connect_database(db_file)

        if conn is not None:
            self.create_table(table, conn)
            tmp = self.insert_into_database(tableName, conn, data)
            conn.close()
            return tmp
        return None

    def extractAllData(self, tableName, order_by="reg"):
        conn = self.connect_database()

        if conn is not None:
            cur = conn.execute(
                "SELECT * FROM {} ORDER BY {}".format(tableName, order_by)
            )
            data = cur.fetchall()
            conn.close()
            return data
        return None

    def delete_all_data(self, db_file, tableName):
        conn = self.connect_database(db_file)

        if conn is not None:
            # conn.commit()
            cur = conn.cursor()
            cur.execute(
                """
                DELETE FROM {};
                """.format(
                    tableName
                )
            )
            conn.commit()
            conn.close()


if __name__ == "__main__":
    pass
