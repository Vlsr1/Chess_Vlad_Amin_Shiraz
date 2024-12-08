# tests/conftest.py
import pytest
import threading
from chess_project.server import start_server

@pytest.fixture(scope="session", autouse=True)
def run_server():
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()
    yield
    server_thread.join(timeout=1)

