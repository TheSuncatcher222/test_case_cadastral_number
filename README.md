# Тестовое задание для Antipoff Group

## Этапы выполнения

✅ Написать сервис, который принимает запрос с указанием кадастрового номера, широты и долготы, эмулирует отправку запроса на внешний сервер, который может обрабатывать запрос до 60 секунд. Затем должен отдавать результат запроса. Считается, что внешний сервер может ответить `true` или `false`.

- ✅ Данные запроса на сервер и ответ с внешнего сервера должны быть сохранены в БД. Нужно написать API для получения истории всех запросов/истории по кадастровому номеру.

- ✅ Сервис должен содержать следующие эндпоинты:
    - ✅ `/query` - для получения запроса
    - ✅ `/result` - для отправки результата
    - ✅ `/ping` - проверка, что  сервер запустился
    - ✅ `/history` - для получения истории запросов

- ✅ Добавить Admin панель.

- ✅ Сервис завернуть в Docker.

- ✅ Добавить документацию.

- ✅ Добавить тесты.

- ✅ * В качестве дополнительного задания. Можно добавить дополнительный сервис, который будет принимать запросы первого сервиса и эмулировать внешний сервер.

## Инструкция по развертке

Для функционирования проекта необходимо иметь базу данных PostgreSQL и Redis. Рекомендуется разворачивать проект в Docker согласно имеющемуся `docker-compose.yml`.

1. Склонировать проект в целевую папку

```
git clone git@github.com:TheSuncatcher222/cadastral_number_test_case.git
```

2. Перейти в `cadastral_number_test_case/backend`

```
cd cadastral_number_test_case/backend
```

3. Создать файл переменных окружения из примера

```
cp .env.example .env
```

4. Изменить переменные окружения на основании шаблона (если необходимо)

```
(на примере редактора Nano)
nano .env
```

5. Вернуться в корневую папку проекта (на уровень выше)

```
cd ..
```

6. Запустить Docker Compose сборку (убедитесь, что `docker daemon` запущен в системе!)

```
docker-compose up
```

7. Проверить доступность проекта на `localhost:8000`

```
http://localhost:8000/
# login: admin, password: admin
http://localhost:8000/admin/
```

## Лицензия

MIT

**Какая лицензия, это же тестовое!**

## Разработчик

[Кирилл Свидунович](https://github.com/TheSuncatcher222/)
