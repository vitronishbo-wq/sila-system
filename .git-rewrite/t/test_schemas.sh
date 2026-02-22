#!/bin/bash
cd /home/truman/dev/sila-system/apps/backend
source .venv/bin/activate
python3 -c "
from core.schemas import UserRead
from modules.auth.models.user import User
print('UserRead fields:', [f for f in UserRead.model_fields.keys()])
print('User columns:', [c.name for c in User.__table__.columns])
"
