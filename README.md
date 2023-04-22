# YaMDb

### YaMDb это API, который собирает отзывы  пользователей на произведения и формирует их рейтинг.

Благодаря отзывам пользователей вы всегда сможете найти какой-нибудь годный контент для себя.

---

УСТАНОВКА ПРИЛОЖЕНИЯ:

1. Клонировать репозиторий и перейти в него в командной строке:
   git clone git@github.com:Faithdev21/api_yamdb
   cd api_yamdb
2. Cоздать и активировать виртуальное окружение:
   python3 -m venv env
   source env/bin/activate
3. Установить зависимости из файла requirements.txt:
   python3 -m pip install --upgrade pip
   pip install -r requirements.txt
4. Выполнить миграции:
   python3 manage.py migrate
5. Запустить проект:
   python3 manage.py runserver

---

ПРИМЕРЫ ЗАПРОСОВ

`/api/v1/categories/`  
GET -  Получение списка всех категорий  
POST - Добавление новой категории  

`/api/v1/genres/`  
GET - Получение списка всех жанров  
POST - Добавление жанра  

`/api/v1/genres/{slug}/`  
DELETE - Удаление жанра  

`/api/v1/titles/`  
GET - Получение списка всех произведений  
POST - Добавление произведения  

`/api/v1/titles/{titles_id}/`  
GET - Получение информации о произведении  
DELETE - Удаление произведения  

`/api/v1/titles/{title_id}/reviews/`  
GET - Получение списка всех отзывов  
POST - Добавление нового отзыва  

`/api/v1/titles/{title_id}/reviews/{review_id}/`  
GET - Полуение отзыва по id  
PATCH - Частичное обновление отзыва по id  
DELETE - Удаление отзыва по id  

`/api/v1/titles/{title_id}/reviews/{review_id}/comments/`  
GET - Получение списка всех комментариев к отзыву  
POST - Добавление комментария к отзыву  
PATCH - Частичное обновление комментария к отзыву  
DELETE - Удаление комментария к отзыву  

`/api/v1/auth/signup/`  
POST - Регистрация нового пользователя.  

`/api/v1/auth/token/`  
POST - Получение JWT-токена в обмен на username и confirmation code.  

`/api/v1/users/`  
GET - Получить список всех пользователей.  

`/api/v1/users/`  
POST - Добавить нового пользователя.  

`/api/v1//users/{username}/`  
GET - Получить пользователя по username.  

`/api/v1//users/{username}/`  
PATCH - Изменить данные пользователя  

`/api/v1//users/{username}/`  
DELETE - Удалить пользователя по username.  

`/api/v1/users/me/`  
GET - Получить данные своей учетной записи  

`/api/v1/users/me/`  
PATCH - Изменить данные своей учетной записи  

---

АВТОРЫ ПРОЕКТА:  
🚀️ Егор Лоскутов https://github.com/Faithdev21  
🚀️ Иван Березный https://github.com/IBEREZNYI  
🚀️ Павел Пономарев https://github.com/permanganatoff  

---

СТЕК ТЕХНОЛОГИЙ:  
При создании проекта были использованы следующие технологии:  

> Python, Django, djangorestframework, pytest, Simple JWT, GIT  
