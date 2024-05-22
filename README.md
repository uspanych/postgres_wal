## Запуск проекта
docker compose up --build
## Описание
В рамках лабораторных работ №1, 2 был поднят кластер сосотоящий из 3 контейнеров с Postgresql, где 1-й контейнер - это мастер, 2-й реплика, а 3-й арбитр.
Агент написан на Python, установлен в образ для контенеров с Бд. В роли арбитра выступает веб сервер написанный на языке Python. 
## Сценарий
Раз в квант времени агент на слейве проверяет досутпность мастера, в случае отсутствия ответа,
слейв вызывает метод АПИ у веб сервера для проверки. В ответ на вызов метода возвращается json {"Master": "Alive"} - Живой, {"Master": "Dead"} - Помер. В случае отключения мастера - происходит промоут до мастера на слейве.

## Тестирование
При синхронной релпикации - запросы не терялись, при асинхронной потерялись 62 значения.