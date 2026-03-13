import requests
import sys

# URL might need to be localhost or sila-backend depending on where we run it.
# Since we run from host (wsl), localhost:8000 should work as port is mapped.
BASE_URL = "http://localhost:8000/api/v1"

def test_login(email, password, label):
    print(f"\n🔵 Teste: {label} ({email})")
    try:
        resp = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
        if resp.status_code == 200:
            print("   ✅ Login bem-sucedido!")
            data = resp.json()
            token = data.get("access")
            if not token:
                print("   ⚠️ Token 'access' não encontrado na resposta.")
                print(f"   Resposta: {data}")
                return False
            
            print(f"   🔑 Token: {token[:15]}...")
            
            # Test /me
            headers = {"Authorization": f"Bearer {token}"}
            me_resp = requests.get(f"{BASE_URL}/auth/me", headers=headers)
            if me_resp.status_code == 200:
                user_data = me_resp.json()
                print(f"   👤 Usuário Identificado: {user_data.get('email')} [{user_data.get('level')}]")
                return True
            else:
                print(f"   ❌ Falha em /me: {me_resp.status_code}")
                print(f"   Conteúdo: {me_resp.text}")
                return False
        else:
            print(f"   ❌ Login Falhou: {resp.status_code}")
            print(f"   Conteúdo: {resp.text}")
            return False
            
    except Exception as e:
        print(f"   🔥 Erro de conexão: {e}")
        return False

if __name__ == "__main__":
    print(f"🔍 Verificando Login Central no Endpoint {BASE_URL}")
    
    # 1. Usuário Central via Seed
    res1 = test_login("admin_central_central@sila.gov.ao", "admin123", "Central User (Seed)")
    
    # 2. Usuário Admin Bootstrap (Fallback)
    res2 = test_login("admin@sila.gov.ao", "admin123", "Admin User (Bootstrap)")

    if res1 or res2:
        sys.exit(0)
    else:
        sys.exit(1)
