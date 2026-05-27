# Защищенный файловый менеджер

Это защищенное веб-приложение для безопасного хранения, шифрования и управления пользовательскими файлами. Все сделано с фокусом на *безопасность*

## Что входит в проект:
* **Backend:** Python 3.10, FastAPI, Pydantic
* **База данных:** получился только JSON
* **Инфраструктура:** Docker, Docker Compose
* **Безопасность:** * Шифрование файлов в покое (Fernet / AES)
  * Хэширование паролей (Passlib / bcrypt)
  * Аутентификация и авторизация (JWT)
  * Генерация UUID для имен файлов
* **Крутые прооверки:** GitHub Actions (CI/CD), pre-commit hooks, SAST (Bandit), DAST (OWASP ZAP)

## ⚙️ Установка и запуск (One-Command Run)

Проект полностью контейнеризирован. Для запуска требуется только установленный Docker и Docker Compose.

1. **Клонируйте репозиторий:**
   ```bash
   git clone [https://github.com/Futaecivoh/CS_Futaecivoh.git](https://github.com/Futaecivoh/CS_Futaecivoh.git)
   cd CS_Futaecivoh
