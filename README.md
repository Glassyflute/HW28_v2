# Домашнее задание 28

## Описание задач и действий
- Файлы с данными в формате csv сконвертированы в json, скорректированы данные внутри отдельных файлов для успешной 
- загрузки в БД postgres.
- Подключена postgres БД через использование docker и образа с контейнером, пользователь и пароль postgres по умолчанию.
- После применения изначальных миграций на создание пустых таблиц в БД использована команда loaddata для загрузки 
- данных в таблицы БД с помощью файлов с фикстурами (с полями fields, model, pk), в которые были конвертированы 
- файлы json с данными.
- Данные в БД основаны на использовании 4 таблиц: category, location, user, ad. Каждая из 4 моделей зарегистрирована
- внутри файла admin.py в папке приложения ads, детали по моделям и полям указаны в файле models.py. 
- Модель Объявления (ad) имеет ForeignKey на Категорию (category) и Пользователя (user), а модель Пользователя
- внутри себя имеет связь с несколькими адресами (location, m2m).
- 
- Картинки в объявлении загружаются в папку media/images.
- 
- В папке приложения Avito обновлены файлы settings.py, urls.py.
- Для пагинации в файле settings.py выбран лимит TOTAL_ON_PAGE = 5 для вывода данных постранично. При выводе информации
- в GET запросе указывается общее кол-во элементов, кол-во страниц. 
- 
- В папке приложения ads создан отдельный python package для urls по выводу информации на объявления, категорию и 
- пользователя. В основном файле urls.py внутри папки приложения Avito сделаны отсылки на каждое направление.
- 
- При выводе списка элементов через GET запросы и ListView используется сортировка с помощью order_by. 
- Категории сортируются по названию, Пользователи - по username в обратном алфавитном порядке.
- Объявления сортируются по убыванию цены.
- 
- POST, PATCH для Пользователя позволяют добавить новый адрес.
- GET запросы на Пользователя показывают общее кол-во опубликованных объявлений по данному пользователю. Список 
- пользователей показывает информацию по среднему значению, минимуму и максимуму по возрасту всех пользователей, а 
- также аналогичную статистику по цене объявлений по пользователю с помощью aggregate.
- 
- ываыв
- 