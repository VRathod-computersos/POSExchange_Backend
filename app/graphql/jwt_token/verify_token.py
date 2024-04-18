from jwt_token.jwt_verify import verify_jwt_token

def verify_token(token):
    payload = {"token": token}
    responseFromJWTVerify = verify_jwt_token(payload)
    return {
        "Response": responseFromJWTVerify["body"]["Response"],
        "is_logged_in": responseFromJWTVerify["body"]["is_logged_in"],
        "client_id": responseFromJWTVerify["body"]["client_id"],
    }
