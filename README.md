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

#### ClientState

```
{
    1: "active",
    2: "lost"
}
```

#### OperationType

```
{
    1: "service",
    2: "goodSell",
    3: "spend",
    4: "employeePayment"
}
```

#### ContactType

```
{
    1: "phone",
    2: "email",
    3: "vk",
    4: "instagram",
    5: "facebook",
    6: "telegram",
    7: "whatsapp",
    8: "viber",
    9: "other"
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
{
    "login": "логин юзера"
}
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
{
"officeId": id отделения
}
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
            "id": id сотрудника,
            "name": "имя сотрудника",
            "role": роль пользователя из Roles. Может быть officeAdmin или master (1 или 3 соответственно)
            "pictureUrl": "ссылка на фотку сотрудника",
            "workHours": количество рабочих часов
        }
    ],
    "officeId": id отделения,
    "state": состояние смены из SessionState (по логике метода, здесь всегда должно быть open),
    "operations": [ // массив операций, проведённых за смену
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
            "id": id сотрудника,
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
        "state": OfficeState
    }
]
```

#### GetEmployees

Возвращает список сотрудников. Записи должны быть отсортированы сначала по статусу (вверху активные), потом по имени по алфавиту.

##### URL

```
api/GetEmployees/
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
        "pictureUrl": url фотографии юзера,
        "state": UserState,
        "servicesPercent": процент от продажи услуг,
        "goodsPercent": процент от продажи товаров,
        "masterCategory": категория мастера. Может быть null
        "roles": [список ролей пользователя из Roles]
    }
]
```

#### EditSession

Открыть / отредактировать смену.

##### URL

```
api/EditSession/
```

##### Вход

```
{
    "dateOpened": "дата и время открытия смены в формате dd.mm.yyyy HH:MM",
    "employees": [ //Список мастеров и админов с часами работы
        {
            "id": id сотрудника,
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
        "id": id услуги,
        "name": название услуги,
        "prices" {
            id категории мастера: цена,
            ...
        }
    }
]
```

#### GetEmployeePaymentTypes

Возвращает список типов платежей сотрудникам.

##### URL

```
api/GetEmployeePaymentTypes/
```

##### Вход

```
{}
```

##### Выход

```
[
    {
        "id": id типа платежа сотруднику,
        "name": название типа платежа сотруднику,
        "sum": дефолтная сумма платежа
    }
]
```

#### EditOperations

Создание / редактирование операций.

##### URL

```
api/EditOperations/
```

##### Вход

Files: список фотографий стрижки. Может быть пустым

Data:

```
[
    {
        "operationType": 'service',
        "officeId": id отделения,
        "sessionId": id смены,
        "serviceId": id услуги,
        "startDatetime": Дата и время начала в формате dd.mm.yyyy HH:MM,
        "finishDatetime": Дата и время заверешения в формате dd.mm.yyyy HH:MM,
        "adminId": id администратора,
        "masterId": id мастера,
        "clientId": id клиента,
        "cashSum": Сумма налички,
        "cashlessSum": Сумма безнала,
        "discountSum": Сумма скидки,
        "adminBonus": Сумма премии админа,
        "masterBonus": Сумма премии мастера,
        "clientRating": Оценка клиента от 1 до 10 или null,
        "review": Отзыв клиента,
        "comment": Комментарий
    },
    {
        "operationType": 'goodSell',
        "officeId": id отделения,
        "sessionId": id смены,
        "goodsIds": Список id товаров, которые были проданы по данной операции,
        "datetime": Дата и время продажи в формате dd.mm.yyyy HH:MM,
        "adminId": id администратора,
        "masterId": id мастера,
        "clientId": id клиента,
        "cashSum": Сумма налички,
        "cashlessSum": Сумма безнала,
        "discountSum": Сумма скидки,
        "adminBonus": Сумма премии админа,
        "masterBonus": Сумма премии мастера,
        "comment": Комментарий
    },
    {
        "operationType": 'spend',
        "officeId": id отделения,
        "sessionId": id смены,
        "expenseTypeId": id типа расхода,
        "datetime": Дата и время расхода в формате dd.mm.yyyy HH:MM,
        "sum": Сумма,
        "comment": Комментарий
    },
    {
        "operationType": 'employeePayment',
        "officeId": id отделения,
        "sessionId": id смены,
        "employeeId": id сотрудника,
        "type": Тип выплаты сотруднику,
        "datetime": Дата и время выплаты в формате dd.mm.yyyy HH:MM,
        "sum": Сумма,
        "comment": Комментарий
    }
]
```

##### Выход

Если сохранение прошло успешно

```
[
    {
        "id": id операции
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
    "serviceId": Тип услуги,
    "startDatetime": Дата и время начала в формате dd.mm.yyyy HH:MM,
    "finishDatetime": Дата и время заверешения в формате dd.mm.yyyy HH:MM,
    "adminId": id администратора,
    "masterId": id мастера,
    "clientId": id клиента,
    "cashSum": Сумма налички,
    "cashlessSum": Сумма безнала,
    "discountSum": Сумма скидки,
    "adminBonus": Сумма премии админа,
    "masterBonus": Сумма премии мастера,
    "score": Оценка клиента от 1 до 10 или null,
    "clientRating": Отзыв клиента,
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

#### GetGoodsOperation

Возвращает операцию по продаже товара.

##### URL

```
api/GetGoodsOperation/
```

##### Вход

```
{
    "id": id операции по продаже товара
}
```

##### Выход

Если есть операция с таким id

```
{
    "id": id операции,
    "officeId": id отделения,
    "sessionId": id смены,
    "type": [Типы товаров],
    "datetime": Дата и время продажи в формате dd.mm.yyyy HH:MM,
    "adminId": id администратора,
    "masterId": id мастера,
    "clientId": id клиента,
    "cashSum": Сумма налички,
    "cashlessSum": Сумма безнала,
    "discountSum": Сумма скидки,
    "adminBonus": Сумма премии админа,
    "masterBonus": Сумма премии мастера,
    "comment": Комментарий
}
```

Если произошла ошибка

```
{
    "error": "Нет операции по продаже товара с таким id."
    "stackTrace": stackTrace
}
```

#### GetSpendOperation

Возвращает операцию по расходу.

##### URL

```
api/GetSpendOperation/
```

##### Вход

```
{
    "id": id операции по расходу
}
```

##### Выход

Если есть операция с таким id

```
{
    "id": id операции,
    "officeId": id отделения,
    "sessionId": id смены,
    "expenseTypeId": id Типа расхода,
    "datetime": Дата и время расхода в формате dd.mm.yyyy HH:MM,
    "sum": Сумма,
    "comment": Комментарий
}
```

Если произошла ошибка

```
{
    "error": "Нет операции по расходу с таким id."
    "stackTrace": stackTrace
}
```

#### GetEmployeePaymentOperation

Возвращает операцию по выплате сотруднику.

##### URL

```
api/GetEmployeePaymentOperation/
```

##### Вход

```
{
    "id": id операции по выплате сотруднику
}
```

##### Выход

Если есть операция с таким id

```
{
    "id": id операции,
    "officeId": id отделения,
    "sessionId": id смены,
    "employeeId": id сотрудника,
    "type": Тип выплаты сотруднику,
    "datetime": Дата и время выплаты в формате dd.mm.yyyy HH:MM,
    "sum": Сумма,
    "comment": Комментарий
}
```

Если произошла ошибка

```
{
    "error": "Нет операции по выплате сотруднику с таким id."
    "stackTrace": stackTrace
}
```


#### GetSessionsWithOperations

Возвращает список сессий с операциями. Сессии выбираются по фильтру. Любое из полей в фильтре может быть null, тогда фильтр по этому полю не накладывается. Смены отсортированы по убыванию даты открытия (сначала новые). Операции отсортированы по возрастанию даты (сначала старые).

##### URL

```
api/GetSessionsWithOperations/
```

##### Вход

```
{
    "dateFrom": дата от в формате dd.mm.yyyy. HH:MM,
    "dateTo": дата до в формате dd.mm.yyyy. HH:MM,
    "operationType": [массив OperationType],
    "employeeIds": [массив id сотрудников],
    "clientIds": [массив id клиентов]
}
```

##### Выход

```
[
    {
        "id": id смены,
        "dateOpened": "дата и время открытия смены в формате dd.mm.yyyy HH:MM",
        "dateClosed": "дата и время закрытия смены в формате dd.mm.yyyy HH:MM",
        "employees": [ //Список мастеров и админов с часами работы
            {
                "id": id сотрудника,
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
]
```

#### EditClient

Создание / редактирование клиента.

##### URL

```
api/EditClient/
```

##### Вход

Files: фото клиента

Data:

```
{
    "name": имя клиента,
    "state": ClientState,
    "contacts": [ // Контакты. Может быть несколько одного типа
        {
            "type": ContactType,
            "value": "значение контакта. Любая строка"
            "comment": "Комментарий. Любая строка"
        }
    ],
    "comment": коментарий
}
```

##### Выход

Если сохранение прошло успешно

```
[
    {
        "id": id клиента
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

#### GetClient

Возвращает клиента.

##### URL

```
api/GetClient/
```

##### Вход

```
{
    "id": id клиента
}
```

##### Выход

Если есть клиент с таким id

```
{
    "id": id клиента,
    "name": имя клиента,
    "state": ClientState,
    "contacts": [ // Контакты
        {
            "type": ContactType,
            "value": значение контакта
            "comment": комментарий
        }
    ],
    "comment": коментарий
}
```

Если произошла ошибка

```
{
    "error": "Нет клиента с таким id."
    "stackTrace": stackTrace
}
```

#### GetClients

Возвращает список клиентов по фильтру. Если фильтр пустой, возвращает всех клиентов.

##### URL

```
api/GetClients/
```

##### Вход

```
{
    "q": часть имени или контакта клиента 
}
```

##### Выход

```
[
    {
        "id": id клиента,
        "name": имя клиента,
        "state": ClientState,
        "contacts": [ // Контакты
            {
                "type": ContactType,
                "value": значение контакта
                "comment": комментарий
            }
        ],
        "comment": коментарий
    }
]
```
