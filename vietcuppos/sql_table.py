from local_database import SQLRawCommand, DatabaseSQLite
import datetime

db = DatabaseSQLite()
dt = datetime.datetime.now()

# CREATE TABLE
#db.create_table(SQLRawCommand.create_table_user, conn)
conn = db.connect_database()
db.create_table(SQLRawCommand.create_table_report, conn)
conn = db.connect_database()
db.create_table(SQLRawCommand.create_table_store, conn)
conn = db.connect_database()
db.create_table(SQLRawCommand.create_table_menu, conn)
conn = db.connect_database()
db.create_table(SQLRawCommand.create_table_bill, conn)

# INSERT DATA to TABLE
m1 = ("22cfd", "Dark Coffee", 19.99, 299)
m2 = ("23cfd", "Milk Coffee", 29.99, 199)
m3 = ("52cfd", "Special Coffee", 39.99, 99)
conn = db.connect_database()
db.insert_into_database("Menus", conn, m1)
conn = db.connect_database()
db.insert_into_database("Menus", conn, m2)
conn = db.connect_database()
db.insert_into_database("Menus", conn, m3)
print(db.db_dir)
