import graphene
import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)
from ...database.connection import (
    connect_to_database_master_db,
)


def connect_to_company(client_id):
    print(client_id,":Client Id is ")
    print("Into the company database connection")
    with connect_to_database_master_db() as master_db:
        
        with master_db.cursor() as master_cursor:
            master_cursor.execute(
                f"SELECT company_Name FROM client_master WHERE client_id = %s",
                (client_id,),
            )
            print("After executing query for getting comapny name")
        
            company_name = master_cursor.fetchone()[0]
            print("Again after the comapny name", company_name)
            master_cursor.close()

    if not company_name:
        raise ValueError(f"No company found for Client_ID: {client_id}")

    # return company_name
    return company_name

