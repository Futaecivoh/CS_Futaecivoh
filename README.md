# 🛡️ Secure File Manager (SFM)

**Secure File Manager** — это защищенное веб-приложение (REST API) для безопасного хранения, шифрования и управления пользовательскими файлами. Проект разработан с фокусом на информационную безопасность (AppSec) и контейнеризацию.

## 🚀 Технологический стек
* **Backend:** Python 3.10, FastAPI, Pydantic
* **База данных:** SQLite / PostgreSQL (в зависимости от окружения)
* **Инфраструктура:** Docker, Docker Compose
* **Безопасность:** * Шифрование файлов в покое (Fernet / AES)
  * Хэширование паролей (Passlib / bcrypt)
  * Аутентификация и авторизация (JWT)
  * Защита от Path Traversal (генерация UUID для имен файлов)
* **DevSecOps:** GitHub Actions (CI/CD), pre-commit hooks, SAST (Bandit), DAST (OWASP ZAP)

## ⚙️ Установка и запуск (One-Command Run)

Проект полностью контейнеризирован. Для запуска требуется только установленный Docker и Docker Compose.

1. **Клонируйте репозиторий:**
   ```bash
   git clone [https://github.com/ВАШ_НИК/CS_Futaecivoh.git](https://github.com/ВАШ_НИК/CS_Futaecivoh.git)
   cd CS_Futaecivoh
