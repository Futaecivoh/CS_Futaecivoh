# Защита Docker

## WHOAMI(??????)
Мы сделали терминал в терминале и теперь руководим контейнером от лица пользователя без root прав
<img width="694" height="220" alt="photo_2026-05-04_21-43-32" src="https://github.com/user-attachments/assets/4bb5e1d5-1c28-4bba-875f-c826d76bfc30" />

## Проверка уязвимостей
Воспользовались сканером Trivy и увидели возможные уязвимости в нашем Docker. Уязвимости есть даже `high`... *Но это же окей для тестового?*
### Первый скриншот
<img width="812" height="415" alt="photo_2026-05-04_21-43-37" src="https://github.com/user-attachments/assets/8360e51d-64b5-4ba1-a6c7-8c52d7df301e" />
### Второй скриншот
<img width="791" height="371" alt="photo_2026-05-04_21-43-40" src="https://github.com/user-attachments/assets/4804a9ba-2e03-4922-bb73-0530448e0e0b" />

## Проверка скачивания файлов
Теперь все файлы будут сохранятся от имени пользователя 1000, который грустный и не знает ничего об root правах. Грустячка(
Пост дал сигнал 200, все загружено!
<img width="962" height="640" alt="photo_2026-05-04_22-00-14" src="https://github.com/user-attachments/assets/7290d518-0cc7-4862-9f50-6ea45f209888" />

