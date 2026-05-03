# Отчет по IDOR, RBAC

## Контроль доступа
Чтобы не допустить возможность получения доступа злоумышленником файлов, к которым он не имеет доступа, мы настроили **разделенный контроль доступа** и добавили **проверки на права доступа**
### Dependency Injection
Чтобы не прописывать сотню раз `if` `else`, мы просто сделаем отдельную функцию

`def get_current_user(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )
    return user`
### Сделаем отдельный скрипт проверки всего этого

`def test_security():
    s = requests.Session()`

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

## Тестирование
<img width="630" height="194" alt="photo_2026-05-03_19-48-08" src="https://github.com/user-attachments/assets/53665199-1279-4810-b643-18b6db419754" />

