from graphene import ObjectType, Mutation, String, Boolean, Int, List
import graphene
import os
import sys
import random
import smtplib
import bcrypt
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ..models.connect_to_company import connect_to_company

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from ...database.connection import (
    connect_to_database_master_db,
    connect_to_database_company,
)




from ..types.registerSeller import RegisterInput, POSField
from components.send_email import send_email


# load_dotenv()

otp_storage = {}


# function to generate otp
def generate_otp():
    return str(random.randint(100000, 999999))


# function to send the otp to user's email
# def send_email(email, otp):
#     sender_email = os.getenv('sender_email')
#     sender_password = os.getenv('sender_email_pwd')

#     subject = "OTP Verification"
#     body = f"Your OTP for email verification is: {otp}"

#     message = MIMEText(body)
#     message["Subject"] = subject
#     message["From"] = sender_email
#     message["To"] = email

#     print(f'Email Address: {email}')
#     print(f"Sender Email Address: {sender_email}")
#     with smtplib.SMTP("smtp.office365.com", 587) as server:
#         # server.ehlo()
#         server.starttls()
#         server.ehlo()
#         server.login(sender_email, sender_password)
#         server.sendmail(sender_email, [email], message.as_string())


# function to save otp of perticular email
def save_otp(email, otp):
    # otp_storage[email] = otp
    with connect_to_database_master_db() as master_db:
        with master_db.cursor() as master_cursor:
            master_cursor.execute(
                "UPDATE client_master SET OTP = %s WHERE email_eddress = %s",
                (
                    otp,
                    email,
                ),
            )


# function to verfity otp of perticular email
def verify_otp(email, user_otp):
    saved_otp = otp_storage.get(email)
    return saved_otp == user_otp


def email_body(
    email,
    company_name,
    pos_name,
    license_key,
    number_of_license,
    registration_date,
    end_date,
):
    # email subject
    subject = "license key with other details"
    # email message
    email_message = f"""
        Hello {company_name}, \n\n
        I am writing to provide you with the details of your POS license: \n\n
        Company Name: {company_name}\n
        POS Name: {pos_name}\n
        license Key: {license_key}\n
        Number of licenses: {number_of_license}\n
        Registration Date: {registration_date}\n
        Subscription End Date: {end_date}\n\n 
        If you have any questions or need further assistance, feel free to reach out.\n\n
        Best regards,\n
        POS Doctor Support Team
    """

    try:
        send_email(email, subject, email_message)
        print("After send emails")
    except Exception as e:
        return str(e)


# is_email_verified = graphene.Boolean(required=True)


# Class to send to OTP to user's email address
class OTPEmailSentMutations(Mutation):
    class Arguments:
        email = String(required=True)

    otp_generated = Boolean()
    otp_message = String()
    email_sent = Boolean()
    email_message = String()

    def mutate(self, info, email):
        otp_generated = None
        otp_message = None
        email_sent = None
        email_message = None
        with connect_to_database_master_db() as master_db:
            with master_db.cursor() as master_cursor:
                # to check the email is already exist in Client_Master
                master_cursor.execute(
                    "SELECT COUNT(*) FROM client_master WHERE email_address = %s",
                    (email,),
                )
                result_data = master_cursor.fetchone()

                # if email exists in Client_Master table
                if result_data[0] > 0:
                    otp_generated = False
                    otp_message = "Email is already registered. Please log in or try different email"
                else:
                    # if email is not exist in Client_Master table
                    try:
                        # calling generate_otp function
                        otp = generate_otp()

                        # calling save_otp function to save OTP in local storage
                        save_otp(email, otp)

                        otp_generated = True
                        otp_message = "OTP generated successfully"
                    except Exception as Err:
                        otp_generated = False
                        otp_message = "Failed to generate OTP"
                        print("Error Occured:", str(Err))
                    try:
                        # to send otp to the user's email address
                        send_email(email, otp)
                        email_sent = True
                        email_message = "Email with OTP sent successfully"
                    except Exception as Err:
                        email_sent = False
                        email_message = "Failed to Send OTP to your email"
                        print("Error Occured:", str(Err))

            return OTPEmailSentMutations(
                otp_generated=otp_generated,
                otp_message=otp_message,
                email_sent=email_sent,
                email_message=email_message,
            )


# class to verify OTP
class VerifyOTPEmailMutation(Mutation):
    class Arguments:
        email = String(required=True)
        otp = String(required=True)

    otp_verified = Boolean()
    otp_message = String()

    def mutate(self, info, email, otp):
        if verify_otp(email, otp):
            return VerifyOTPEmailMutation(
                otp_verified=True, otp_message="OTP Verified Successfully"
            )
        else:
            return VerifyOTPEmailMutation(
                otp_verified=False,
                otp_message="Failed to Verify OTP. Please click on resend OTP",
            )


# class to register user if email is verified
class RegisterUser(Mutation):
    class Arguments:
        input_data = RegisterInput(required=True)

    success = Boolean()
    message = String()
    client_id = Int()
    database_created = Boolean()
    database_message = String()
    license_email_sent = Boolean()
    license_email_message = String()
   

    def mutate(self, info, input_data):
        email = input_data.email
        password = input_data.password
        license_key = input_data.license_key
        company_name = input_data.company_name
        company_name = company_name.replace(" ", "_")
        pos_id = input_data.pos_id
        client_id = input_data.client_id
        tenant_id = input_data.tenant_id
        whether_free = input_data.whether_free
        trial_end_date = input_data.trial_end_date
        number_of_license = input_data.number_of_license

        success = False
        message = None
        database_created = False
        database_message = None
        license_email_sent = False
        license_email_message = None

        # is_email_verified = input_data.is_email_verified

        with connect_to_database_master_db() as master_db:
            with master_db.cursor() as master_cursor:
                # Hash the password using bcrypt
                hashed_password = bcrypt.hashpw(
                    password.encode("utf-8"), bcrypt.gensalt()
                )
                
                # check if the company is already registered
                master_cursor.execute(
                    "SELECT COUNT(*) FROM client_master WHERE company_Name = %s",
                    (company_name,),
                )

                result = master_cursor.fetchone()[0]
                print("It is near result", result)
                if result:
                    company_name = connect_to_company(client_id)
                    print(company_name, "This is company name")
                    with connect_to_database_company(company_name) as com_db:
                        with com_db.cursor() as com_cursor:
                            registration_date = datetime.utcnow()
                            # if company's database exist check email is already registered or not
                            com_cursor.execute(
                                "SELECT COUNT(*) FROM login_info WHERE email_address = %s",
                                (email,),
                            )
                            data = com_cursor.fetchone()[0]
                          
                            if data:
                                success = False
                                message = "Email is already registered. Please log in."
                                
                                client_id = None

                                database_created = False
                                database_message = "Company's Database Aleady exist in our Healthcheck database"
                            else:
                                # if email is not registered then store data in Login_Info table
                                com_cursor.execute(
                                    "INSERT INTO login_info (email_address, password, registration_date) VALUES (%s, %s, %s)",
                                    (
                                        email,
                                        hashed_password.decode("utf-8"),
                                        registration_date,
                                    ), 
                                )
                            
                                com_db.commit()

                                # store the license details in client_master table
                                master_cursor.execute(
                                    "SELECT company_name, pos_id, license_key, number_of_license, registration_date, end_date FROM client_master WHERE company_name = %s",
                                    (company_name,),
                                )
                                client_data = master_cursor.fetchall()

                                for data in client_data:
                                    company_name = data[0]
                                    pos_id = data[1]
                                    license_key = data[2]
                                    number_of_license = data[3]
                                    registration_date = data[4]
                                    end_date = data[5]

                                    master_cursor.execute(
                                        "SELECT pos_name FROM pos_master WHERE pos_id = %s",
                                        (pos_id,),
                                    )
                                    print("before pos name")
                                    pos_name = master_cursor.fetchone()[0]
                                    print(pos_name)
                                    # try:
                                    #     # call function to send email with license key and other details
                                    #     email_body(
                                    #         email,
                                    #         company_name,
                                    #         pos_name,
                                    #         license_key,
                                    #         number_of_license,
                                    #         registration_date,
                                    #         end_date,
                                    #     )
                                    #     license_email_sent = True
                                    #     license_email_message = "Email sent successfully with license key and other details"
                                    # except Exception as e:
                                    #     license_email_sent = False
                                    #     license_email_message = str(e)
                                    #     print("Error: ", str(e))
                                

                                success = True
                                
                                message = "Registeration successfull."
                                client_id = client_id
                                database_created = False
                                database_message = "Company's database already exist in our Healthcheck database"
                                license_email_sent = license_email_sent
                                license_email_message = license_email_message
                else:
                    try:
                        # if company's database not exist then create
                        with connect_to_database_company(None) as com_db:
                            with com_db.cursor() as com_cursor:
                                registration_date = datetime.utcnow()
                                com_cursor.execute(
                                    f"CREATE DATABASE IF NOT EXISTS {company_name}"
                                )
                                com_cursor.execute(f"USE {company_name}")

                                # to create a login_info table
                                com_cursor.execute(
                                    f"""
                                        CREATE TABLE IF NOT EXISTS login_info (
                                            client_id INT DEFAULT {client_id},
                                            email_address VARCHAR(50),
                                            password VARCHAR(255),
                                            device_id VARCHAR(255),
                                            device_name VARCHAR(255),
                                            is_logged_in VARCHAR(10),
                                            last_login_time DATETIME,
                                            last_logout_time DATETIME,
                                            registration_date DATETIME,
                                            otp INT
                                        )
                                    """
                                )
                                com_db.commit()

                                # store the login credentials in company's database in Login_Info table
                                com_cursor.execute(
                                    "INSERT INTO login_Info (email_Address, password, registration_date) VALUES (%s, %s, %s)",
                                    (
                                        email,
                                        hashed_password.decode("utf-8"),
                                        registration_date,
                                    ),
                                )
                                
                                com_db.commit()

                                # store the license key details in Client_Master table
                                master_cursor.execute(
                                    "INSERT INTO client_master (client_id, company_name, pos_id, license_key, number_of_license, tenant_id, whether_free, registration_date, end_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                    (
                                        client_id,
                                        company_name,
                                        pos_id,
                                        license_key,
                                        number_of_license,
                                        tenant_id,
                                        whether_free,
                                        registration_date,
                                        trial_end_date,
                                    ),
                                )
                                print("Hello this is Checkpoint")
                                master_db.commit()

                                master_cursor.execute(
                                    "SELECT pos_name FROM pos_master WHERE pos_id = %s",
                                    (pos_id,),
                                )
                                pos_name = master_cursor.fetchone()[0]
                                print(pos_name)
                                # try:
                                #     email_body(
                                #         email,
                                #         company_name,
                                #         pos_name,
                                #         license_key,
                                #         number_of_license,
                                #         registration_date,
                                #         trial_end_date,
                                #     )
                                #     license_email_sent = True
                                #     license_email_message = "Email sent successfully with license key and other details"
                                #     print("Inside try")
                                # except Exception as e:
                                #     license_email_sent = False
                                #     license_email_sent = str(e)

                                event = {"client_id": client_id, "is_logged_in": True}

                                success = True
                                message = "Registration successful"
                                client_id = client_id
                                database_created = True
                                database_message = (
                                    f"Database created for company name: {company_name}"
                                )
                                license_email_sent = license_email_sent
                                license_email_message = license_email_message

                    except Exception as e:
                        print("Error: ", e)

                return RegisterUser(
                    success=success,
                    message=message,
                    client_id=client_id,
                    database_created=database_created,
                    database_message=database_message,
                    license_email_sent=license_email_sent,
                    license_email_message=license_email_message,
                )


class Mutation(ObjectType):
    otp_sent = OTPEmailSentMutations.Field()
    verify_otp = VerifyOTPEmailMutation.Field()
    register_user = RegisterUser.Field()


class Query(ObjectType):
    pos_system = List(POSField)

    def resolve_pos_system(self, info):
        pos_list = []
        with connect_to_database_master_db() as master_db:
            with master_db.cursor() as master_cursor:
                master_cursor.execute(
                    "SELECT pos_id, pos_name, paid_plan_code, free_plan_code, pos_description FROM pos_master"
                )
                pos_data = master_cursor.fetchall()
                for pos in pos_data:
                    pos_id = pos[0]
                    pos_name = pos[1]
                    paid_plan_code = pos[2]
                    free_plan_code = pos[3]
                    pos_description = pos[4]
                    pos_list.append(
                        {
                            "pos_id": pos_id,
                            "pos_name": pos_name,
                            "paid_plan_code": paid_plan_code,
                            "free_plan_code": free_plan_code,
                            "pos_description": pos_description,
                        }
                    )
                return pos_list
