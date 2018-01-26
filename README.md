# Дешборд статистики по проектам оптимизатора

На дешборде показываются проекты, добавленные в оптимизатор в ходе проекта "Внедрение оптимизатора". [Описание проекта](https://docs.google.com/spreadsheets/d/10rX8nQ9NWIWpzO5hJngOogmo5ML2uA_FvKX2fMYCqKI/edit?usp=sharing).

Развёрнут на [http://192.168.4.158:8899/](http://192.168.4.158:8899/)

## Разработка
Бэк на Python Flask. Фронт на Vue.js.

Чтобы запустить фронт локально:
```
cd front
npm install
npm run dev
```


## Выкладка
1. Cбилдить фронт 
```
cd front
npm run build
```

2. Cкопировать app.py и файлы из front/dist сюда [http://192.168.4.158:8888/tree/Demin/AutopilotDashboard](http://192.168.4.158:8888/tree/Demin/AutopilotDashboard)

3. Перезапустить сервер: остановить Server.ipynb. Затем зайти в него и выполнить первый блок через ctrl+enter. Также можно выполнить команду в баше ```python app.py``` в этой папке.

