from app.core.security import get_password_hash, verify_password, create_access_token


plain_password = "mysecret123"
hashed = get_password_hash(plain_password)
print("Hashed password:", hashed)


is_valid = verify_password("mysecret123", hashed)
print("Password is valid?", is_valid)


token = create_access_token({"sub": "user1"})
print("JWT Token:", token)
