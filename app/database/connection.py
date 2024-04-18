
import mysql.connector
# import pyodbc
# from dotenv import load_dotenv
import os

# load_dotenv()


# Mysql database credentials
master_db = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "Master_DB",
}

# Mysql database credentials
# company_db = {
#     "host": "localhost",
#     "user": "root",
#     "password": "root",
#     "database": None,
# }

# # Mysql database credentials
# master_db = {
#     "host": "healthcheck",
#     "user": "GHC",
#     "password": "Computer@123",
#     "database": "Master_DB",
# }

# # Credentials to connect the specific company
company_db = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": None,
}




# SQL Server credentials
# sql_server_db = {
#     "driver": "ODBC Driver 17 for SQL Server",
#     "host": None,
#     "port": None,
#     "database": None,
#     "user": None,
#     "password": None,
# }


# to connect to the Master_DB
def connect_to_database_master_db():
    try:
        db = mysql.connector.connect(**master_db)
        print(f"Connected to MySQL Server - Master_DB")
        return db
    except mysql.connector.Error as Err:
        print(f"Error Occurred: {Err}")
        db = None


# to connect to the specific company
def connect_to_database_company(company_name):
    # Updating the company_db dictionary with the dynamic company name
    company_db["database"] = company_name
   
    try:
        db = mysql.connector.connect(**company_db)
        print(f"Connected to MySQL Server - Company DB ({company_name})")
        return db
    except mysql.connector.Error as Err:
        print(f"Error Occurred: {Err}")
        db = None


# to connect to the SQL Server
# def data_for_sql_server(sql_server, sql_port, sql_database, sql_username, sql_password):
#     sql_server_db["host"] = sql_server
#     sql_server_db["port"] = sql_port
#     sql_server_db["database"] = sql_database
#     sql_server_db["user"] = sql_username
#     sql_server_db["password"] = sql_password

    # connection_string = (
    #     f"DRIVER={sql_server_db['driver']};"
    #     f"SERVER={sql_server_db['host']};"
    #     f"PORT={sql_server_db['port']};"
    #     f"DATABASE={sql_server_db['database']};"
    #     f"UID={sql_server_db['user']};"
    #     f"PWD={sql_server_db['password']}"
    # )
    # return connection_string


# def connect_to_sql_server():
#     try:
#         db = pyodbc.connect(**sql_server_db)

#         print(f"Connected to SQL Server Database : ",sql_server_db["database"])
#         return db
#     except pyodbc.Error as err:
#         print(f"Error Occurred: {err}")
#         db = None
