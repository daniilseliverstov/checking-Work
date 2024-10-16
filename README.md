# Проект "Счетчик ДЗ"

**Описание**

Эта программа — это простое приложение для отслеживания времени и проверки заданий с помощью графического интерфейса пользователя (GUI). Приложение имеет основное окно с таймером, который можно запустить, приостановить или остановить. Также в окне есть кнопки для обозначения правильных и неправильных ответов на проверяемые задания, а также кнопка для отмены последнего действия (правильного или неправильного ответа).

Приложение отображает статистику, такую как количество проверенных заданий и процент правильных ответов. Кроме того, в нижней части окна есть кнопка "Результаты", которая открывает новое окно, отображающее историю результатов, сохраненных в базе данных SQLite.

## Содержание

- [Функции](#функции)
- [Установка](#установка)
- [Использование](#использование)

### Функции

- Запуск, пауза и остановка таймера
- Отмечать правильные и неправильные ответы на задания
- Отмена последнего действия (правильного или неправильного ответа)
- Отображение статистики (количество проверенных заданий и процент правильных ответов)
- Сохранение результатов в базе данных SQLite
- Просмотр истории результатов и их удаление

### Установка

1. Клонируйте этот репозиторий:

2. Установите необходимые пакеты:

`pip install tkinter`


### Использование

- Запустите таймер, нажав кнопку "Начать".
- Отмечайте правильные ответы, нажав кнопку "Верно".
- Отмечайте неправильные ответы, нажав кнопку "Неверно".
- Отмените последнее действие (правильный или неправильный ответ), нажав кнопку "Мисклик".
- Приостановите таймер, нажав кнопку "Пауза".
- Продолжите таймер, нажав кнопку "Продолжить".
- Остановите таймер и сохраните результаты, нажав кнопку "Завершить".
- Просмотрите историю результатов, нажав кнопку "Результаты".
- Ненужные результаты можно удалить
