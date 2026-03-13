
import sys
sys.path.append("/app")

from apps.backend.app.modules.identity.models.user import User
from sqlalchemy import inspect

def debug_user():
    try:
        mapper = inspect(User)
        print(f"Mapper for User: {mapper}")
        for rel in mapper.relationships:
            print(f"Relationship: {rel.key} -> {rel.target}")
    except Exception as e:
        print(f"Error inspecting User: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_user()
