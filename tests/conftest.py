import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from routers import users


# чистим хранилище
@pytest.fixture(autouse=True)
def reset_users():
    users.db.clear()
    users._next_id = 0
    yield
    users.db.clear()
    users._next_id = 0
