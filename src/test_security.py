import requests

BASE_URL = "http://127.0.0.1:8000"

def login(session, username, password):
    resp = session.post(
        f"{BASE_URL}/login",
        data={"username": username, "password": password}
    )
    return resp.status_code == 200

def test_security():
    s = requests.Session()

    print("=== Тест 1 ===")
    login(s, "alice", "123")
    r = s.get(f"{BASE_URL}/files/2")
    assert r.status_code == 404, f"Ожидался 404, получили {r.status_code}"
    print("Пройден")

    print("=== Тест 2 ===")
    r = s.get(f"{BASE_URL}/files/1")
    assert r.status_code == 200
    print("Пройден")

    print("=== Тест 3 ===")
    login(s, "admin", "000")
    r = s.delete(f"{BASE_URL}/files/2")
    assert r.status_code == 200
    print("Пройден")

    r = s.get(f"{BASE_URL}/files/2")
    assert r.status_code == 404
    print("Файл действительно удалён")

    print("\nТесты пройдены")

if __name__ == "__main__":
    test_security()
