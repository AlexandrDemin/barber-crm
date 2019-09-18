# CRM для барбершопа

Простая CRM для барбершопа на python3 flask и vue.js

## Разработка

Бэк на Python3 Flask. Фронт на Vue.js.

Установка зависимостей:

```
pip3 install -r requirements.txt
```

Запуск веба:

```
python3 -m app
```

Билд фронта:

```
cd front
npm install
npm run build
```

Файлы фронта после билда складываются в папку dist, их оттуда отдаёт веб-сервер фласка.

## API для фронта

### Описание

API по принципу JSON RPC. Все вызовы через POST запрос. На входе JSON, на выходе JSON.

Токен для авторизации в апишке должен быть в куке.

Некоторые методы могут отдавать ошибки. Тогда в теле ответа отдавать 

```
{
    "error": "Человеческое описание ошибки",
    "stackTrace": stacktrace
}
```

Некоторые методы могут отдавать предупреждения. Тогда в теле ответа отдавать дополнительно

```
{
    …
    "Info": "Текст предупреждения"
}
```

### Типы данных

#### Roles

```
{
    1: "officeAdmin",
    2: "manager",
    3: "master"
}
```

#### UserState

```
{
    1: "works",
    2: "doesntWork"
}
```

#### OfficeState

```
{
    1: "works",
    2: "doesntWork"
}
```

#### SessionState

```
{
    1: "open",
    2: "closed"
}
```

#### OperationType

```
{
    1: "service",
    2: "itemSell",
    3: "spend",
    4: "employeePayment"
}
```

### Методы

#### GetUserData

Возвращает данные текущего юзера.

##### URL

```
api/GetUserData/
```

##### Вход

```
{}
```

##### Выход

```
{
    "name": "Имя пользователя",
    "pictureUrl": "ссылка на фотку юзера",
    "roles": ["массив ролей пользователя из Roles"]
}
```

#### GetCurrentSession

Возвращает текущую (открытую) смену. Если нет текущей смены, возвращает пустой объект.

##### URL

```
api/GetCurrentSession/
```

##### Вход

```
{}
```

##### Выход

Если нет открытой смены

```
{}
```

Иначе

```
{
    "id": id смены,
    "dateOpened": "дата и время открытия смены в формате dd.mm.yyyy HH:MM",
    "dateClosed": null,
    "employees": [ //Список мастеров и админов с часами работы
        {
            "Id": id сотрудника,
            "name": "имя сотрудника",
            "role": роль пользователя из Roles. Может быть officeAdmin или master (1 или 3 соответственно)
            "pictureUrl": "ссылка на фотку сотрудника",
            "workHours": количество рабочих часов
        }
    ],
    "officeId": id отделения,
    "state": состояние смены из SessionState (по логике метода, здесь всегда должно быть open),
    "Operations": [ // массив операций, проведённых за смену
        {
            "operationType": OperationType,
            … // все параметры операции в зависимости от типа
        }
    ] 
}
```

#### GetSession

Возвращает смену по id. Если нет такой смены, возвращает ошибку.

##### URL

```
api/GetSession/
```

##### Вход

```
{
    "id": id смены,
    "withOperations": true / false // Нужно ли возвращать список операций по смене
}
```

##### Выход

Если нет смены с таким id

```
{
    "error": "Нет смены с таким id"
}
```

Иначе

```
{
    "id": id смены,
    "dateOpened": "дата и время открытия смены в формате dd.mm.yyyy HH:MM",
    "dateClosed": "дата и время закрытия смены в формате dd.mm.yyyy HH:MM",
    "employees": [ //Список мастеров и админов с часами работы
        {
            "Id": id сотрудника,
            "name": "имя сотрудника",
            "role": роль пользователя из Roles. Может быть officeAdmin или master (1 или 3 соответственно)
            "pictureUrl": "ссылка на фотку сотрудника",
            "workHours": количество рабочих часов
        }
    ],
    "officeId": id отделения,
    "state": состояние смены из SessionState,
    "Operations": [ // массив операций, проведённых за смену. Если withOperations
        {
            "operationType": OperationType,
            … // все параметры операции в зависимости от типа
        }
    ] 
}
```

#### GetOffices

Возвращает список отделений. Записи должны быть отсортированы сначала по статусу (вверху активные), потом по названию по алфавиту.

##### URL

```
api/GetOffices/
```

##### Вход

```
{}
```

##### Выход

```
[
    {
        "id": id отделения,
        "name": название отделения,
        "status": OfficeState
    }
]
```

#### GetAdmins

Возвращает список администраторов офисов. Записи должны быть отсортированы сначала по статусу (вверху активные), потом по имени по алфавиту.

##### URL

```
api/GetAdmins/
```

##### Вход

```
{}
```

##### Выход

```
[
    {
        "id": id юзера,
        "name": имя юзера,
        "photoUrl": url фотографии юзера,
        "status": UserState
    }
]
```

#### GetMasters

Возвращает список администраторов офисов. Записи должны быть отсортированы сначала по статусу (вверху активные), потом по имени по алфавиту.

##### URL

```
api/GetMasters/
```

##### Вход

```
{}
```

##### Выход

```
[
    {
        "id": id юзера,
        "name": имя юзера,
        "photoUrl": url фотографии юзера,
        "status": UserState
    }
]
```

#### EditSession

Открыть / отредактировать смену.

##### URL

```
api/OpenSession/
```

##### Вход

```
{
    "dateOpened": "дата и время открытия смены в формате dd.mm.yyyy HH:MM",
    "employees": [ //Список мастеров и админов с часами работы
        {
            "Id": id сотрудника,
            "name": "имя сотрудника",
            "role": роль пользователя из Roles. Может быть officeAdmin или master (1 или 3 соответственно)
            "workHours": количество рабочих часов
        }
    ],
    "officeId": id отделения
}
```

##### Выход

Если операция прошла успешно

```
{
    "id": id смены
}
```

Если произошла ошибка

```
{
    "error": "Произошла ошибка при сохранении смены."
    "stackTrace": stackTrace
}
```

#### CloseSession

Закрыть смену.

##### URL

```
api/CloseSession/
```

##### Вход

```
{
    "id": id смены
    "officeId": id отделения
}
```

##### Выход

Если операция прошла успешно

```
{
    "id": id смены
}
```

Если произошла ошибка

```
{
    "error": "Произошла ошибка при сохранении смены."
    "stackTrace": stackTrace
}
```

#### GetServicesPrices

Возвращает список услуг с ценами.

##### URL

```
api/GetServicesPrices/
```

##### Вход

```
{}
```

##### Выход

```
[
    {
        "Id": id услуги,
        "name": название услуги,
        "prices" {
            id категории мастера: цена,
            ...
        }
    }
]
```

#### EditServiceOperation

Создание / редактирование операции по услуге.

##### URL

```
api/EditServiceOperation/
```

##### Вход

Files: список фотографий стрижки

Data:

```
{
    "officeId": id отделения,
    "sessionId": id смены,
    "type": Тип услуги,
    "started": Дата и время начала в формате dd.mm.yyyy HH:MM,
    "finished": Дата и время заверешения в формате dd.mm.yyyy HH:MM,
    "adminId": id администратора,
    "masterId": id мастера,
    "clientId": id клиента,
    "cashSum": Сумма налички,
    "cashlessSum": Сумма безнала,
    "discountSum": Сумма скидки,
    "score": Оценка клиента от 1 до 10 или null,
    "review": Отзыв клиента,
    "comment": Комментарий
}
```

##### Выход

Если сохранение прошло успешно

```
[
    {
        "Id": id операции
    }
]
```

Если произошла ошибка

```
{
    "error": "Произошла ошибка при сохранении операции."
    "stackTrace": stackTrace
}
```

#### GetServiceOperation

Возвращает операцию по услуге.

##### URL

```
api/GetServiceOperation/
```

##### Вход

```
{
    "id": id операции по услуге
}
```

##### Выход

Если есть операция по услуге с таким id

```
{
    "id": id операции по услуге,
    "officeId": id отделения,
    "sessionId": id смены,
    "type": Тип услуги,
    "started": Дата и время начала в формате dd.mm.yyyy HH:MM,
    "finished": Дата и время заверешения в формате dd.mm.yyyy HH:MM,
    "adminId": id администратора,
    "masterId": id мастера,
    "clientId": id клиента,
    "cashSum": Сумма налички,
    "cashlessSum": Сумма безнала,
    "discountSum": Сумма скидки,
    "score": Оценка клиента от 1 до 10 или null,
    "review": Отзыв клиента,
    "photoUrls": [список ссылок на фотографии стрижки],
    "comment": Комментарий
}
```

Если произошла ошибка

```
{
    "error": "Нет операции по услуге с таким id."
    "stackTrace": stackTrace
}
```
