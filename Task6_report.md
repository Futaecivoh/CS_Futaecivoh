# Отчет по защите от XSS и настройке CSP

## Уязвимость
Я создал искусственно файл уязвимости и вот что из этого вышло. `Alert` **бахнул** как нельзя кстати
<img width="1280" height="648" alt="photo_2026-05-02_00-45-41" src="https://github.com/user-attachments/assets/8908b3bb-64c2-4ffe-9efc-47dee93e707a" />

## Санитизация
Увидев уязвимости, мы пошли исправлять их двумя способами. Созданием индивидуальных проверок и Санитизации `bleach` и **CSP**. Это исправило все ошибки и даже вывело отчет об исправленных ошибках. Чтобы это сделать мне, кстати, пришлось ещё раз убрать всю защиту(
<img width="523" height="371" alt="photo_2026-05-02_00-45-45" src="https://github.com/user-attachments/assets/ffa6e0d1-28a1-4494-ab2e-a5a719690298" />

***CSP*** 
<img width="539" height="573" alt="photo_2026-05-02_00-45-56" src="https://github.com/user-attachments/assets/f9c29dca-d816-4534-8316-3cad4c93446e" />

***Скриншот заблокированной атаки*** 
<img width="555" height="481" alt="photo_2026-05-02_00-45-59" src="https://github.com/user-attachments/assets/0446a91b-121f-49ba-b9f5-712317b9e7a4" />
