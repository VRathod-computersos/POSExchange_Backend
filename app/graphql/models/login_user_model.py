from graphene import String, InputObjectType
class LoginInput(InputObjectType):
    email = String(required=True)
    password = String(required=True)
    device_id = String()
    device_name = String()
    
class LogoutInput(InputObjectType):
    email = String(required=True)
    device_id = String()
    device_name = String()