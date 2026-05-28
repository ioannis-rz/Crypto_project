import secrets

# PEPPER Generation Script
pepper = secrets.token_hex(16)
# export PASSWORD_PEPPER=pepper # en consola antes de correr la aplicación
print(pepper)