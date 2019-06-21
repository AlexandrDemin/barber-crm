# Инструмент для фильтрации запросов по количеству конкурентов в SEO КП

С помощью этого инструмента спецы предпродажки находят запросы, по которым мало конкурентов в выдаче, и удаляют их в SEO КП.
Сервис получает данные из монги SEO КП, се кеша, базы регионов, сервиса Яндекс Икс и ещё на сайты конкурентов ломится (вытаскивает тайтл, дескрипшн и фавикон).

Развёрнуто всё это здесь http://client.ingate/Offers/FilterRivals/

## Разработка
Бэк на Python Flask. Фронт на Vue.js.

Запуск веба:
```
python -m app
```

Билд фронта:
```
cd front
npm install
npm run build
```

Файлы фронта после билда складываются в папку dist, их оттуда отдаёт веб-сервер фласка.