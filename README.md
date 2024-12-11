# PP2
# Проект на Django с использованием Docker

Это пример проекта на Django, который использует Docker для развертывания. В этом проекте используется PostgreSQL в качестве базы данных.

## Требования

- Docker
- Docker Compose

## Установка

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/Chernov279/PP2.git
   cd ваш_репозиторий
    ```

2. Создайте виртуальное окружение и активируйте его (по желанию, если не используете Docker):
   ```bash
    python -m venv venv
    source venv/bin/activate  # на Linux/MacOS
    venv\Scripts\activate     # на Windows
    ```
3. Установите зависимости:

   ```bash
    pip install -r requirements.txt
   ```
4. Настройте базу данных (PostgreSQL):

Создайте файл .env в корне проекта и добавьте настройки для базы данных. Ниже код для примера:
   ```bash
    SECRET_KEY=django-insecure-+12345678909876540+kinay5791o9khoo6mit7-i3r01-zf
    DB_ENGINE=django.db.backends.postgresql
    DB_NAME=PP2
    DB_USER=postgres
    DB_PASSWORD=postgres
    DB_HOST=localhost
    DB_PORT=5432
   ```

## Запуск с помощью Docker

1. Сборка контейнеров:

Для начала вам нужно собрать Docker-образы. Выполните следующую команду:
   ```bash
    docker-compose build
   ```
Эта команда соберет контейнеры для вашего веб-приложения и базы данных, но на этом этапе миграции базы данных еще не будут выполнены.
2. Примените миграции базы данных:

После сборки контейнеров необходимо применить миграции для правильной настройки базы данных. Выполните команду:
   ```bash
docker-compose exec web python app/manage.py migrate
   ```
Эта команда применяет все миграции, обновляя схему базы данных.

3. Запустите контейнеры:

В корне проекта выполните команду:
   ```bash
docker-compose up
   ```
Эта команда:

 Соберет Docker-образы.
 Запустит контейнеры для веб-приложения (Django) и базы данных (PostgreSQL).

Теперь проект доступен по адресу http://localhost:8000.

## модели, адаптированные под формат dbdiagram.io:
Table custom_user {
  slug varchar(255) [pk]
  email varchar(255) [unique]
  username varchar(255)
  first_name varchar(30)
  last_name varchar(30)
  is_active boolean [default: true]
  is_staff boolean [default: false]
  created_at datetime
  updated_at datetime
}

Table project {
  id int [pk, increment]
  name varchar(255) [not null]
  description text
  created_at datetime
  last_updated_at datetime
  created_by_id int [ref: > custom_user.id]
}

Table column {
  id int [pk, increment]
  project_id int [ref: > project.id]
  name varchar(255)
  position int
  color varchar(7) [default: "#ffffff"]
  created_at datetime
  last_updated_at datetime
}

Table task {
  id int [pk, increment]
  column_id int [ref: > column.id]
  project_id int [ref: > project.id]
  title varchar(255)
  description text
  status varchar(50)
  assigned_to_id int [ref: > custom_user.id]
  created_at datetime
  last_updated_at datetime
}

Table task_log {
  id int [pk, increment]
  task_id int [ref: > task.id]
  message text
  created_at datetime
}

Table project_user {
  id bigint [pk, increment]
  project_id int [ref: > project.id]
  user_id int [ref: > custom_user.id]
  status varchar(15) [default: "member"]
  indexes {
    (project_id, user_id) [unique]
  }
}