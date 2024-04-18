import json
import jwt, datetime, time
import os
# from dotenv import load_dotenv

# load_dotenv()

#to create the JWT Token
def generate_jwt_token(event):
    client_id = event['client_id']
    is_logged_in = event['is_logged_in']
    print("Data: ", client_id, is_logged_in)
    flag = ''
    token = ''
    secretKey = 'XM9s7+hD2X!^2VJMCvCQayUp@EQ6xz#qz9h'
    # secretKey = os.getenv('secretKey')
    payload = {
        'iss': 'auth0',
        'client_id': client_id,
        'is_logged_in': is_logged_in,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=365)
    }

    try:
        token = jwt.encode(payload, secretKey, algorithm='HS256')
        flag = 'true'
        print(token)
    except:
        flag = 'false'

    response = {
        'token' : token,
        'status' : flag
    }

    return {
        'statusCode': 200,
        'body': response
    }

# event_data = {
#     'client_id': '123',
#     'is_logged_in': True
# }
# result = generate_jwt_token(event_data)
# print(result)
