# Курсовая работа №4. 

### Описание проекта
- Установка зависимостей
```shell
pip install -r requirements.txt
```

- Создание моделей (очистит БД и создаст все модели, указанные в импорте)
```shell
python create_tables
```

- Загрузка данных в базу
```shell
python load_fixture
```
Скрипт читает файл fixtures.json и загружает данные в базу. Если данные уже загружены - выводит соответсвующее сообщение. 

### Содержание проекта
- основной файл run.py, который запускает приложение
- в папке project:
  - dao - здесь файлы классов DAO с методами доступа к данным (Data Access Object) из таблиц, а также папка с моделями и схемами сериализации структуры данных таблиц.
  - service - файлы классов сервисов - бизнес логика. Сюда импортируются DAO классы из пакета dao и модели из dao.model
  - tools - файл с функцией хеширования пароля
  - views - файлы с вьюшками API, представления для обработки запросов:
    - auths.py - для авторизации
    - directors.py - для режиссеров
    - genres.py - для жанров
    - movies.py - для фильмов
    - users.py - для пользователей,

  - config.py - файл с конфигурациями приложения 
  - constants.py - файл с константами
  - server.py - файл для создания работающего приложения  
  - setup_db.py - подключение к БД, чтобы импортировать БД без зацикливания
  - utils.py - файл содержит вспомогательные функции.


implemented.py - файл, где названы переменные используемых классов и методов DAO и сервисов, чтобы использовать их везде.

project.db - таблица БД
