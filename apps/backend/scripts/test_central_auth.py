import requests

BASE_URL = "http://localhost:8000/api/v1"
# We'll try admin123 first as per user request, and fallback to sila123 if needed
payloads = [
    {"username": "admin@sila.gov.ao", "password": "admin123"},
    {"username": "admin@sila.gov.ao", "password": "sila123"},
    {"username": "admin.central.angola.1@sila.gov.ao", "password": "sila123"}
]


def test_login():
    token = None
    user_email = None

    for payload in payloads:
        print(f"尝试登录: {payload['username']}...")
        try:
            response = requests.post(f"{BASE_URL}/auth/login", data=payload)
            if response.status_code == 200:
                token = response.json().get("access_token")
                user_email = payload['username']
                print(f"✅ Token obtido para {user_email}: {token[:20]}...")
                break
            else:
                print(f"❌ Falha no login ({response.status_code}): {response.text}")
        except Exception as e:
            print(f"❌ Erro de conexão: {e}")
            break

    if not token:
        print("❌ Não foi possível obter token com as credenciais fornecidas.")
        return

    # 2. Verificar Perfil (Nível de Acesso)
    headers = {"Authorization": f"Bearer {token}"}
    try:
        # User requested /auth/me, but usually statistics/me or auth/me depends on implementation
        # I'll check /auth/me first
        me_response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        if me_response.status_code != 200:
            # Try statistics/me as mentioned in previous context (Conversation 7755361f...)
            me_response = requests.get(f"{BASE_URL}/statistics/me", headers=headers)

        if me_response.status_code == 200:
            user_data = me_response.json()
            print(f"\n👤 Dados do Usuário:")
            print(f"   Email: {user_data.get('email')}")
            # The field might be 'level' as per model or 'admin_level' as per user request
            level = user_data.get('level') or user_data.get('admin_level')
            print(f"   Nível: {level}")
            print(
                f"   Região: {user_data.get('region_name') or user_data.get('region', {}).get('name')}")

            if level == "CENTRAL":
                print("\n✨ VERIFICAÇÃO BEM-SUCEDIDA: Nível CENTRAL confirmado.")
            else:
                print(f"\n⚠️ AVISO: Nível esperado: CENTRAL, Nível obtido: {level}")
        else:
            print(f"❌ Erro ao obter perfil ({me_response.status_code}): {me_response.text}")
    except Exception as e:
        print(f"❌ Erro ao consultar perfil: {e}")


if __name__ == "__main__":
    test_login()
