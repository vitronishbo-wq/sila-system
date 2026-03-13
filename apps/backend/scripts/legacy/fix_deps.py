import os

path = "app/api/deps.py"
if os.path.exists(path):
    with open(path, 'r') as f:
        content = f.read()
    
    # Substitui a tipagem de int para str no user_id
    new_content = content.replace('user_id: int = payload.get("sub")', 'user_id: str = str(payload.get("sub"))')
    new_content = new_content.replace('user_id: int = token_data.sub', 'user_id: str = str(token_data.sub)')
    
    with open(path, 'w') as f:
        f.write(new_content)
    print("✅ app/api/deps.py atualizado para suportar UUID!")
else:
    print("❌ Arquivo app/api/deps.py não encontrado no diretório atual.")
