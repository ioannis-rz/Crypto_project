import secrets

# PEPPER Generation Script
pepper = secrets.token_hex(16)
print(pepper)