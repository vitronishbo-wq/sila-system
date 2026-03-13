import os

path = "app/core/territory/models/territory.py"
with open(path, 'r') as f:
    content = f.read()

# Garante que o tablename seja locations
content = content.replace('__tablename__ = "territories"', '__tablename__ = "locations"')

# Garante que a ForeignKey aponte para a tabela correta (locations.id)
if 'ForeignKey("territories.id")' in content:
    content = content.replace('ForeignKey("territories.id")', 'ForeignKey("locations.id")')
elif 'ForeignKey(\'territories.id\')' in content:
    content = content.replace('ForeignKey(\'territories.id\')', 'ForeignKey(\'locations.id\')')

with open(path, 'w') as f:
    f.write(content)
print("✅ Modelo Territory sincronizado com a tabela locations!")
