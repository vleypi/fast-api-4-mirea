# fast api 4

Контрольная работа 4 по дисциплине «Технологии разработки серверных приложений», РТУ МИРЭА.

## О приложении

Сервер на FastAPI с базой данных SQLite, миграциями Alembic, обработкой ошибок и тестами.

Товары хранятся в SQLite, таблица создаётся миграциями, а начальные данные добавляет `seed.py`. Ошибки приложения возвращаются в едином формате: `error` и `detail`. Ошибки валидации приходят списком полей с сообщениями.

Покупка товара и пользователи из `/users` хранятся в памяти и сбрасываются при перезапуске.

## Маршруты

| Метод | Адрес | Что делает |
|---|---|---|
| GET | `/products` | список товаров из базы |
| GET | `/errors/items/{item_id}` | остаток товара, 404 если товара нет |
| POST | `/errors/buy/{item_id}` | покупка, 409 если не хватает остатка |
| POST | `/validation/users` | проверка имени, возраста, почты и пароля |
| POST | `/users` | создание пользователя |
| GET | `/users/{user_id}` | пользователь по id |
| DELETE | `/users/{user_id}` | удаление пользователя |

## Как запустить

Потребуются Git и Python 3.10 или новее.

```bash
git clone https://github.com/vleypi/fast-api-4-mirea.git
cd fast-api-4-mirea
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
python seed.py
uvicorn main:app --reload
```

После запуска сервер доступен по адресу http://localhost:8000, документация по адресу http://localhost:8000/docs. Тесты запускаются командой `pytest -v`.

## Структура

```
fast-api-4-mirea/
├── main.py            приложение и подключение роутеров
├── config.py          настройки из .env
├── database.py        подключение к SQLite и сессии
├── models.py          модель товара SQLAlchemy
├── schemas.py         модели Pydantic
├── exceptions.py      свои ошибки и их обработчики
├── seed.py            начальные товары
├── routers/
│   ├── products.py    товары из базы
│   ├── errors.py      покупка и ошибки 404 и 409
│   ├── validation.py  проверка полей пользователя
│   └── users.py       пользователи в памяти
├── alembic/           миграции
├── tests/             тесты pytest
├── .env.example       пример настроек
├── requirements.txt   зависимости
└── kr4.pdf            задание
```

## Проверка

```bash
curl http://localhost:8000/products

curl -i http://localhost:8000/errors/items/999
curl -i -X POST "http://localhost:8000/errors/buy/2?quantity=5"
curl -X POST "http://localhost:8000/errors/buy/1?quantity=2"

curl -X POST -H "Content-Type: application/json" \
  -d '{"username":"alice","age":25,"email":"a@b.com","password":"qwerty12"}' \
  http://localhost:8000/validation/users

curl -X POST -H "Content-Type: application/json" \
  -d '{"username":"alice","age":25}' http://localhost:8000/users
curl http://localhost:8000/users/1
curl -X DELETE http://localhost:8000/users/1
```
