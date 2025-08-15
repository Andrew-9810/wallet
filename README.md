# wallet
## Описание проекта:
Изменение баланса кошелька.

## Стек технологий:

- Django версии 3.2.16
- Django Rrest Framework версии 3.12.4
- Docker версии 28.3.2

## Запуск проекта с помощью файла docker compose

Перед запуском проекта на вашей машине должен быть установлен Docker.

В директории в которой расположен файл docker-compose.production.yml
выполните команду:

```sudo docker compose -f docker-compose.production.yml up -d```

Выполним миграции:

```sudo docker compose -f docker-compose.production.yml exec wallet python manage.py migrate```

Запустим тесты:

```sudo docker compose -f docker-compose.production.yml exec wallet python manage.py test```

Загрузим в базу данны   х проекта тестовые данные (при необходимости):

```sudo docker compose -f docker-compose.production.yml exec wallet python manage.py loaddata test_data.json```

Соберем статику проекта и пробросим ее в Nginx (для удобства работы в админ-зоне):

```sudo docker compose -f docker-compose.production.yml exec wallet python manage.py collectstatic```

```sudo docker compose -f docker-compose.production.yml exec wallet cp -r /app/collected_static/. /wallet_static/static/```

## Примеры запросов к API
Для получения корректных данных необходимо загрузить тестовые данные в базу данных проекта

Состаяние после загрузки тестовых данных в базу данных:

### Таблица wallet

|pk|amount
|--|------
|1 |10    
|2 |20    

### Получить баланс кошелька
#### GET запрос
```
api/v1/wallets/1
```
#### Ответ от сервера
```
{
    "amount": 10
}
```

### Изменить баланс кошелька, DEPOSIT
#### POST запрос
```
api/v1/wallets/1/operation/
```
##### Тело запроса
```
{
    "operation_type":"DEPOSIT",
    "amount": 1000
}
```
#### Ответ от сервера
```
{
    "amount": 1010
}
```
### Изменить баланс кошелька, WITHDRAW
#### POST запрос
```
api/v1/wallets/2/operation/
```
##### Тело запроса
```
{
    "operation_type":"WITHDRAW",
    "amount": 5
}
```
#### Ответ от сервера
```
{
    "amount": 15
}
```