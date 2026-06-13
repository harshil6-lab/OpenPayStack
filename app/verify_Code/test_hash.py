from app.core.security import hash_password, verify_password    

password = "OpenPay2123"

hashed = hash_password(password)

print("hash : ", hashed)

print("verify: " , verify_password(password,hashed))