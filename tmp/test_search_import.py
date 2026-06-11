import sys, os
sys.path.insert(0, '/home/dev03wsl/sila-system')
sys.path.insert(0, '/home/dev03wsl/sila-system/apps/backend')
os.environ['ENV_MODE'] = 'host'

# Test importing the search router module
try:
    from apps.backend.app.modules.educacao.marketplace.search.api.router import router
    print("SUCCESS: Router imported OK")
except Exception as e:
    import traceback
    print(f"FAIL: {e}")
    traceback.print_exc()
