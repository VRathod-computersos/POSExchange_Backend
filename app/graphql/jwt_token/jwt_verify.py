# coding=utf-8
import json
import jwt
import os
# from dotenv import load_dotenv
# # import boto3
# load_dotenv()

#to verify the JWT Token
def verify_jwt_token(event):
    # secretKey = os.getenv('secretKey')
    secretKey = 'XM9s7+hD2X!^2VJMCvCQayUp@EQ6xz#qz9h'
    token = event['token']
    Response = ''
    decoded = ''

    try:
        decoded = jwt.decode(token, secretKey, iss='auth0', algorithms=['HS256'])
        Response = {
            'Response' : True,
            'client_id' : decoded['client_id'],
            'is_logged_in' : decoded['is_logged_in'],
            'Error' : 'No Error',
        }
    except jwt.ExpiredSignatureError:
        Response = {
            'Response' : False,
            'is_logged_in' : False,
            'client_id': None,
            'Error' : 'Token Expired'   
        }
    except Exception as e:
        Response = {
            'Response' : False,
            'is_logged_in' : False,
            'client_id': None,
            'Error' : e
        }
    return {
        'statusCode': 200,
        'body': Response,
    }

# event = {
#     'token' : 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnRfaWQiOjExMzIsImxvZ2luIjp0cnVlfQ.sUBYxCto7epiif0Maoh6W2pZsLIZVGnUEMWFcYtRIYs'
# }
# result = verify_jwt_token(event)
# print("Result: ", result)