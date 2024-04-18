from graphene import ObjectType, Mutation, String, Boolean, Int, Date
import os
import sys
import bcrypt
from datetime import datetime

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)
from ...database.connection import (
    connect_to_database_master_db,
    connect_to_database_company,
    company_db
)
from jwt_token.jwt_create import generate_jwt_token
# from schema.login_user_model import LoginInput, LogoutInput
# from schema.connect_to_company import connect_to_company
from jwt_token.verify_token import verify_token

from ..models.login_user_model import LoginInput, LogoutInput
from ..models.connect_to_company import connect_to_company
class GetDataFromLicense(Mutation):
    class Arguments:
        license_key = String()

    client_id = Int()
    company_name = String()
    pos_id = Int()
    pos_name = String()
    license_key = String()
    number_of_license = Int()
    tenant_id = String()
    whether_free = String()
    end_date = String()
    success = Boolean()
    message = String()

    def mutate(self, info, license_key):
        with connect_to_database_master_db() as master_db:
            with master_db.cursor() as master_cursor:
                master_cursor.execute(
                    "SELECT client_id, company_name, POS_ID, license_Key, number_Of_license, tenant_id, whether_free, end_date FROM client_master WHERE license_key = %s",
                    (license_key,),
                )

                license_data = master_cursor.fetchall()
                print("license_data: ", license_data)
                if license_data:
                    for data in license_data:
                        client_id = data[0]
                        company_name = data[1]
                        pos_id = data[2]
                        license_key = data[3]
                        number_of_license = data[4]
                        tenant_id = data[5]
                        whether_free = data[6]
                        end_date = data[7]

                        master_cursor.execute(
                            "SELECT pos_name FROM pos_master WHERE pos_id = %s",
                            (pos_id,),
                        )
                        pos_name = master_cursor.fetchone()[0]

                        return GetDataFromLicense(
                            client_id=client_id,
                            company_name=company_name,
                            pos_id=pos_id,
                            pos_name=pos_name,
                            license_key=license_key,
                            number_of_license=number_of_license,
                            tenant_id=tenant_id,
                            whether_free=whether_free,
                            end_date=end_date,
                            success=True,
                            message="Data Fetched Successfully",
                        )
                else:
                    return GetDataFromLicense(
                        success=False, message="license Key is invalid or expired"
                    )


class LoginUser(Mutation):
    class Arguments:
        input_data = LoginInput(required=True)

    client_id = String()
    company_name = String()
    jwt_token = String()
    whether_free = String()
    trial_end_date = Date()
    success = Boolean()
    message = String()
    
    def mutate(self, info, input_data):
        email = input_data.email
        password = input_data.password
        device_id = input_data.device_id
        device_name = input_data.device_name

        client_id = None
        company_name = None
        jwt_token = None
        whether_free = None
        trial_end_date = None
        success = False
        message = ""

        # using the Master_DB database
        with connect_to_database_master_db() as master_db:
            with master_db.cursor() as master_cursor:
                # Check if the email and password match a user in the database
                master_cursor.execute("SELECT client_id FROM client_master")
                client_ids = master_cursor.fetchall()
                print(client_ids)
                found_data = False
                
                for ids in client_ids:
                    if found_data:
                        break
                    client_id = ids[0]

                    # get company name according to the client id
                    company_name = connect_to_company(client_id)
                    print(company_name,"##")
                    with connect_to_database_company(company_name) as com_db:
                    
                        with com_db.cursor() as com_cursor:
                            com_cursor.execute("SELECT email_address, password FROM login_info WHERE email_address = %s LIMIT 1",(email,))
                            user_data = com_cursor.fetchone()
                            print('user_data: ', user_data)

                            if user_data:
                                # user = user_data[0]

                                found_data = True
                                stored_password = user_data[1].encode("utf-8")
                                entered_password = password.encode("utf-8")

                                # User found, check if the password matches
                                if bcrypt.checkpw(entered_password, stored_password):
                                    # return user data and success message
                                    master_cursor.execute(
                                        "SELECT client_id, company_name, number_Of_license, whether_free, end_date FROM client_master WHERE company_name = %s",(company_name,)
                                    )
                                    client_data = master_cursor.fetchone()
                                    if client_data: 
                                        client_id, company_name, number_of_license, whether_free, trial_end_date = client_data
                                        logged_in_at = datetime.utcnow()

                                        print('Number of license: ', number_of_license)
                                        com_cursor.execute(
                                            "SELECT COUNT(*) FROM login_info WHERE is_logged_in = 'YES'"
                                        )
                                        login_count = com_cursor.fetchone()[0]
                                        print('login_count: ', login_count)

                                        if number_of_license > login_count:
                                            is_logged_in = "YES"
                                            
                                            com_cursor.execute("SELECT device_id, device_name FROM login_info WHERE email_address = %s", (email,))
                                            device_data = com_cursor.fetchall()
                                            print('device_data: ', device_data)

                                            device_found = False
                                            for device in device_data:
                                                device_id_data = device[0]
                                                device_name_data = device[1]

                                                if (device_id == device_id_data and device_name == device_name_data):
                                                    device_found = True
                                                    com_cursor.execute("UPDATE login_info SET is_logged_in = %s, last_login_time = %s WHERE email_address = %s AND device_id = %s AND device_name = %s", (is_logged_in, logged_in_at, email, device_id, device_name))
                                                    com_db.commit()
                                                    break 
                                                elif device_id_data is None and device_name_data is None:
                                                    device_found = True
                                                    com_cursor.execute("UPDATE login_info SET is_logged_in = %s, last_login_time = %s, device_id = %s, device_name = %s WHERE email_address = %s", (is_logged_in, logged_in_at, device_id, device_name, email,))
                                                    com_db.commit()
                                                    break

                                            if not device_found:
                                                hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
                                                com_cursor.execute("INSERT INTO login_info (email_address, Password, last_login_time, is_logged_in, device_id, device_name) VALUES (%s, %s, %s, %s, %s, %s)", (email, hashed_password.decode("utf-8"), logged_in_at, is_logged_in, device_id, device_name,))
                                                com_db.commit()
                                                break
                                            # token data
                                            print("Before event")
                                            event = {"client_id": client_id, "is_logged_in": True}

                                            # generate jwt token
                                            response = generate_jwt_token(event)
                                            print("Response for jwt", response)
                                            token = response["body"]["token"]
                                            status = response["body"]["status"]

                                            if status == "true":
                                                jwt_token = token
                                                success = True
                                                message = "Login Successfull"
                                            else:
                                                print("Error generating jwt_token. Status:", status)

                                        else:
                                            # com_cursor.execute("SELECT device_id, device_name FROM Login_Info WHERE email_address = %s",(email,))
                                            com_cursor.execute("SELECT device_id, device_name FROM Login_Info WHERE is_logged_in = 'YES'")
                                            device_data = com_cursor.fetchall()
                                            print('device_data: ', device_data)
                                            devices = [(device[0], device[1]) for device in device_data]
                                            # devices = []
                                            # for device in device_data:
                                            #     device_id = device[0]
                                            #     device_name = device[1]
                                            #     devices.append((device_id, device_name))

                                            success = False
                                            message = f'Cannot log in because the maximum number of devices ({number_of_license}) has been reached. Currently logged in devices: {devices}'
                                    
                                else:
                                    client_id = None
                                    company_name = None
                                    message = "Invalid Password"

                            else:
                                # User not found, return an error message
                                client_id = None
                                company_name = None
                                message = "User not found"

                return LoginUser(
                    client_id=client_id,
                    company_name=company_name,
                    jwt_token=jwt_token,
                    whether_free=whether_free,
                    trial_end_date=trial_end_date,
                    success=success,
                    message=message,
                )


class LogoutUser(Mutation):
    class Arguments:
        input_data = LogoutInput(required=True)

    success = Boolean()
    message = String()

    def mutate(self, info, input_data):
        email = input_data.email
        device_id = input_data.device_id
        device_name = input_data.device_name
        # fetch the token from headers from api requests
        token = info.context["request"].headers.get("jwt_token", "")

        # to verify the token verification
        try:
            token_verification = verify_token(token)
        except Exception as Err:
            print("Error: ", Err)

        if token_verification["Response"] and token_verification["is_logged_in"]:
            print("Verification: ", token_verification)
            client_id = token_verification["client_id"]
            print("Client ID: ", client_id)
            try:
                company_name = connect_to_company(client_id)
                print('company_name: ', company_name)
                with connect_to_database_company(company_name) as com_db:
                    with com_db.cursor() as com_cursor:
                        try:
                            logout_at = datetime.utcnow()
                            com_cursor.execute("UPDATE login_info SET is_logged_in = 'NO', last_logout_time = %s WHERE email_address = %s AND device_id = %s AND device_name = %s", (logout_at, email, device_id, device_name))
                            com_db.commit()
                            success = True
                            message = "Logout Successfully"
                        except Exception as e:
                            success = False
                            message = str(e)

                        return LogoutUser(success=success, message=message)

            except Exception as e:
                print(f"Error: {e}")
                raise Exception(str(e))
        else:
            return {"message": "Unauthorized Access"}



class Mutation(ObjectType):
    login_user = LoginUser.Field()
    logout_user = LogoutUser.Field()
    license_key_details = GetDataFromLicense.Field()

class Query(ObjectType):
    # users = graphene.List(UserType)
    users = String()
