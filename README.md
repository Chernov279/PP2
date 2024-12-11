# PP2
Table Project {
  id int [pk, increment] // ID проекта
  name varchar(255) // Название проекта
  description text // Описание проекта
  created_at datetime [default: now()] // Дата создания
  updated_at datetime [default: now()] // Дата обновления
}

Table Column {
  id int [pk, increment] // ID колонки
  project_id int [ref: > Project.id] // Ссылка на проект
  name varchar(255) // Название колонки
  position int // Позиция колонки на доске
}

Table Task {
  id int [pk, increment] // ID задачи
  column_id int [ref: > Column.id] // Ссылка на колонку
  project_id int [ref: > Project.id] // Ссылка на проект
  title varchar(255) // Заголовок задачи
  description text // Описание задачи
  status varchar(50) // Статус задачи
  assigned_to int [ref: > User.id, null] // Ответственный за задачу (пользователь)
  created_at datetime [default: now()] // Дата создания
  updated_at datetime [default: now()] // Дата обновления
}

Table TaskLog {
  id int [pk, increment] // ID лога задачи
  task_id int [ref: > Task.id] // Ссылка на задачу
  message text // Сообщение лога
  created_at datetime [default: now()] // Дата создания
}

Table User {
  id int [pk, increment] // ID пользователя
  username varchar(255) // Имя пользователя
  email varchar(255) // Электронная почта
  created_at datetime [default: now()] // Дата создания
}

Table ProjectUser {
  id int [pk, increment] // ID записи
  project_id int [ref: > Project.id] // Ссылка на проект
  user_id int [ref: > User.id] // Ссылка на пользователя
}