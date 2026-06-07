import re

with open("test_users_s.txt") as f:
    content = f.read()

# Procura por exceções que não sejam InFailedSQLTransactionError
matches = re.finditer(r"E\s+(sqlalchemy\.exc\.\w+|asyncpg\.exceptions\.\w+): (.*)", content)
found = False
for match in matches:
    error_type = match.group(1)
    message = match.group(2)
    if "InFailedSQLTransactionError" not in error_type:
        print(f"FOUND ORIGINAL ERROR: {error_type}")
        print(f"MESSAGE: {message}")
        found = True
        break

if not found:
    print("NO ORIGINAL ERROR FOUND WITH RE")
