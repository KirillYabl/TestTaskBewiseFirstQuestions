# Вопросы викторины

## Цель проекта

Первая часть тестового задания в компанию bewise на должность python разработчика.

## Как установить

1. Клонировать репозиторий:
```shell
git clone  https://github.com/KirillYabl/TestTaskBewiseFirstQuestions.git
```
2. {Опционально} Создать `.env` и `.dev.env` файлы, согласно примеру файлы `src/env_example.txt`
3. Собрать боевое и тестовое (если нужно запускать тесты) окружения
```shell
docker compose build
docker compose -f docker-compose.dev.yaml build
```

## Как запустить тесты

1. Инициализировать БД и создать в ней таблицы (при первом запуске тестов), может выполняться около минуты
```shell
docker compose -f docker-compose.dev.yaml run --rm testapi python3 db_models.py
```
2. Запустить тесты
```shell
docker compose -f docker-compose.dev.yaml run --rm testapi pytest
```
3. Остановить контейнеры
```shell
docker compose -f docker-compose.dev.yaml down
```

## Как запустить сервис

1. Инициализировать БД и создать в ней таблицы (при первом запуске сервиса), может выполняться около минуты
```shell
docker compose run --rm api python3 db_models.py
```
2. Запустить сервис
```shell
docker compose up
```

После этого сервис запусится по адресу [127.0.0.1:8000](127.0.0.1:8000)

Запросы можно отправлять как с [со страницы документации](http://127.0.0.1:8000/docs#/default/index__post), генерируемой FastApi

Так и непосредственно напрямую, например через curl:
```shell
curl -X POST http://127.0.0.1:8000 -H "Content-Type: application/json" -d '{"questions_num": 5}'
```

## Техническое задание

1. С помощью Docker (предпочтительно - docker-compose) развернуть образ с любой опенсорсной СУБД (предпочтительно - PostgreSQL). Предоставить все необходимые скрипты и конфигурационные (docker/compose) файлы для развертывания СУБД, а также инструкции для подключения к ней. Необходимо обеспечить сохранность данных при рестарте контейнера (то есть - использовать volume-ы для хранения файлов СУБД на хост-машине.
2. Реализовать на Python3 веб сервис (с помощью FastAPI или Flask, например), выполняющий следующие функции:
   1. В сервисе должно быть реализован POST REST метод, принимающий на вход запросы с содержимым вида {"questions_num": integer}. 
   2. После получения запроса сервис, в свою очередь, запрашивает с публичного API (англоязычные вопросы для викторин) https://jservice.io/api/random?count=1 указанное в полученном запросе количество вопросов. 
   3. Далее, полученные ответы должны сохраняться в базе данных из п. 1, причем сохранена должна быть как минимум следующая информация (название колонок и типы данный можете выбрать сами, также можете добавлять свои колонки): 1. ID вопроса, 2. Текст вопроса, 3. Текст ответа, 4. - Дата создания вопроса. В случае, если в БД имеется такой же вопрос, к публичному API с викторинами должны выполняться дополнительные запросы до тех пор, пока не будет получен уникальный вопрос для викторины. 
   4. Ответом на запрос из п.2.a должен быть предыдущей сохранённый вопрос для викторины. В случае его отсутствия - пустой объект. 
3. В репозитории с заданием должны быть предоставлены инструкции по сборке докер-образа с сервисом из п. 2., его настройке и запуску. А также пример запроса к POST API сервиса. 
4. Желательно, если при выполнении задания вы будете использовать docker-compose, SQLAalchemy,  пользоваться аннотацией типов.