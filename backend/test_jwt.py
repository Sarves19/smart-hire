from app.core.jwt import jwt_manager

access = jwt_manager.create_access_token("1")
refresh = jwt_manager.create_refresh_token("1")

print("\nACCESS TOKEN\n")
print(access)

print("\nREFRESH TOKEN\n")
print(refresh)

print("\nDECODED ACCESS TOKEN\n")
print(jwt_manager.decode_token(access))