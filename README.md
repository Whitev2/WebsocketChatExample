

[![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=40&pause=1000&color=373737&background=91C5F4&center=true&vCenter=true&multiline=true&width=1080&height=80&lines=The+websocket+chat)](https://git.io/typing-svg)

## Used technology
- Python 3.11;
- FastApi ( Web framework for building APIs );
- Websocket ( chat )
- Dockerfile and Docker Compose ( containerization );
- PostgreSQL ( database );
- SQLAlchemy ( working with database from Python );
- Alembic ( database migrations made easy );
- Pydantic ( models )

<hr/>


### Установка и запуск

1. Клонировать проект в удобное место:

```sh
git clone https://github.com/Whitev2/bet-test-api.git
```

2. Собрать и запустить контейнеры:
```sh
docker-compose build
```
```sh
docker-compose up
```
<hr/>

### Дополнительные команды


1. Создание файла миграций:
```sh
docker-compose exec app alembic revision --autogenerate -m "init"
```

2. Обновление базы данных:
```sh
docker-compose exec app alembic upgrade head
```

3. Остановка контейнеров:
```sh
docker-compose down
```

4. Запуск контейнеров:
```sh
docker-compose up
```

<hr/>

### API: Документация

- Base_url: http://localhost:8000
- Swagger docs: http://localhost:8000/docs
- Chat ws: ws://localhost:8000/ws/CHAT_ID/USER_ID




<hr/>

### Описание функционала
- Сервис позволяет пользователю проходить регистрацию и авторизацию
- Авторизация построена с помощью jwt токена
- Реализованы чаты с комнатами, чаты не привязаны к юзерам на уровне базы для упрощения разделения на сервисы
- Чтобы подключиться к сокету - необходимо изначально создать комнату с чатом и добавить пользователей, передав их user_id
- Сокет позволяет обмениваться сообщениями в реальном времени
- Реализованы базовые тесты для проверки API

### Что можно доработать
- Разбить на сервисы
- Вместо websockets можно воспользоваться centrifugo сервисом
- Сохранение сообщений должно быть в background task
















