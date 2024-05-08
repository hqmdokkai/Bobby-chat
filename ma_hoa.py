import secrets

# Sinh ra một chuỗi ngẫu nhiên an toàn cho URL
secret_key = secrets.token_urlsafe(24)
print(secret_key)
