# Тестовое задание для Antipoff Group

## Этапы выполнения

- ✅ Написать сервис, который принимает запрос с указанием кадастрового номера, широты и долготы, эмулирует отправку запроса на внешний сервер, который может обрабатывать запрос до 60 секунд. Затем должен отдавать результат запроса. Считается, что внешний сервер может ответить `true` или `false`.

- ✅ Данные запроса на сервер и ответ с внешнего сервера должны быть сохранены в БД. Нужно написать API для получения истории всех запросов/истории по кадастровому номеру.

- ✅ Сервис должен содержать следующие эндпоинты:
    - ✅ `/query` - для получения запроса
    - ✅ `/result` - для отправки результата
    - ✅ `/ping` - проверка, что  сервер запустился
    - ✅`/history` - для получения истории запросов

- ✅ Добавить Admin панель.

- ✅ Сервис завернуть в Docker.

- ✅ Добавить документацию.

- ✅ Добавить тесты.

- ✅ * В качестве дополнительного задания. Можно добавить дополнительный сервис, который будет принимать запросы первого сервиса и эмулировать внешний сервер.

## Инструкция по развертке

To be written...

## Лицензия

MIT

**Какая лицензия, это же тестовое!**

## Разработчик

[Кирилл Свидунович](https://github.com/TheSuncatcher222/)
