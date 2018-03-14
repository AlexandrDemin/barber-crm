#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, abort, render_template, send_from_directory
import json
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__, static_folder='./front/dist/static/', template_folder="./front/dist/")
CORS(app)

@app.route('/static/<path:path>')
def send_files(path):
    return send_from_directory(app.static_folder, path)

@app.route("/api/getStat/<projectId>")
def get_stat(projectId):
    projectId = int(projectId)
    if projectId == None:
        abort(404)
    return json.dumps([
        {
            "projectId": projectId,
            "domain": "refro.ru",
            # выходные
            "holidays": [
                {
                    "from": "17.01.2018",
                    "to": "18.01.2018"
                }
            ],
            # Данные для графика трафика по дням.
            # Прогноз оптимизатора / 30.
            # Если нет данных в какой-то день, null
            "dayTraffic": [
                {
                    "name": "Оптимизатор",
                    "data": {
                        "19.01.2018": 10,
                        "18.01.2018": None,
                        "17.01.2018": 14
                    }
                },
                {
                    "name": "Мотор",
                    "data": {
                        "19.01.2018": 22,
                        "18.01.2018": 18,
                        "17.01.2018": 20
                    }
                },
                {
                    "name": "Факт (только Директ)",
                    "data": {
                        "19.01.2018": 12,
                        "18.01.2018": 143,
                        "17.01.2018": 121
                    }
                }
            ],
            # Данные для графика расходов по дням. Прогноз оптимизатора / 30. Если нет данных в какой-то день, null
            "daySpend": [
                {
                    "name": "Оптимизатор",
                    "data": {
                        "19.01.2018": 332,
                        "18.01.2018": None,
                        "17.01.2018": 490
                    }
                },
                {
                    "name": "Мотор",
                    "data": {
                        "19.01.2018": 210,
                        "18.01.2018": 232,
                        "17.01.2018": 201
                    }
                },
                {
                    "name": "Факт (только Директ)",
                    "data": {
                        "19.01.2018": 221,
                        "18.01.2018": 339,
                        "17.01.2018": 329
                    }
                }
            ],
            # Данные для графика конверсий по дням.
            # Прогноз оптимизатора на месяц, факт в сумме за текущий календарный месяц.
            # Если нет данных в какой-то день, null
            "dayConversions": [
                {
                    "name": "Оптимизатор",
                    "data": {
                        "19.01.2018": 1,
                        "18.01.2018": None,
                        "17.01.2018": 1
                    }
                },
                {
                    "name": "Факт (только Директ)",
                    "data": {
                        "19.01.2018": 0,
                        "18.01.2018": 0,
                        "17.01.2018": 1
                    }
                }
            ],
            # Данные для графика CPC по дням.
            # Прогноз оптимизатора на месяц.
            # Если нет данных в какой-то день, null
            "cpc": [
                {
                    "name": "Оптимизатор",
                    "data": {
                        "19.01.2018": 23,
                        "18.01.2018": None,
                        "17.01.2018": 54
                    }
                },
                {
                    "name": "Факт (только Директ)",
                    "data": {
                        "19.01.2018": 144,
                        "18.01.2018": 160,
                        "17.01.2018": 131
                    }
                }
            ],
            # Данные для графика CPA по дням.
            # Прогноз оптимизатора на месяц.
            # Если нет данных в какой-то день, null
            "cpa": [
                {
                    "name": "Оптимизатор",
                    "data": {
                        "19.01.2018": 23,
                        "18.01.2018": None,
                        "17.01.2018": 54
                    }
                },
                {
                    "name": "Факт (только Директ)",
                    "data": {
                        "19.01.2018": 144,
                        "18.01.2018": 160,
                        "17.01.2018": 131
                    }
                }
            ],
            # Данные для графика месячных расходов.
            # Прогноз оптимизатора на конец месяца = прогноз оптимизатора / 30 * количество дней до конца календарного месяца.
            # Бюджет из Мотора брать как себестоимость услуги рекламный трафик из текущего периода:
                # SELECT p2.costplan * (1 - p2.margin / 100)
                # FROM projectperiod AS p
                # JOIN projectperioddetail AS p2 ON p.id=p2.projectperiodid
                # WHERE p.projectid=2514764 AND p2.servicetype=2015 AND p.enddate IS NOT NULL
                # ORDER BY p.enddate desc
                # LIMIT 1
            # Фактический расход суммируется за текущий календарный месяц
            # Если нет данных в какой-то день, null
            "monthSpend": [
                {
                    "name": "Оптимизатор",
                    "data": {
                        "19.01.2018": 16000,
                        "18.01.2018": None,
                        "17.01.2018": 16000
                    }
                },
                {
                    "name": "Мотор",
                    "data": {
                        "19.01.2018": 38000,
                        "18.01.2018": 38000,
                        "17.01.2018": 38000
                    }
                },
                {
                    "name": "Факт (только Директ)",
                    "data": {
                        "19.01.2018": 25332,
                        "18.01.2018": 23234,
                        "17.01.2018": 22123
                    }
                }
            ],
            # Данные для графика месячного трафика.
            # Прогноз оптимизатора на конец месяца = прогноз оптимизатора / 30 * количество дней до конца календарного месяца.
            # План трафика из Мотора брать из услуги рекламный трафик из текущего периода:
                # SELECT p2.trafficplan
                # FROM projectperiod AS p
                # JOIN projectperioddetail AS p2 ON p.id=p2.projectperiodid
                # WHERE p.projectid=2514764 AND p2.servicetype=2015 AND p.enddate IS NOT NULL
                # ORDER BY p.enddate desc
                # LIMIT 1
            # Фактический трафик суммируется за текущий календарный месяц
            # Если нет данных в какой-то день, null
            "monthTraffic": [
                {
                    "name": "Оптимизатор",
                    "data": {
                        "19.01.2018": 641,
                        "18.01.2018": None,
                        "17.01.2018": 641
                    }
                },
                {
                    "name": "Мотор",
                    "data": {
                        "19.01.2018": 6923,
                        "18.01.2018": 7323,
                        "17.01.2018": 6923
                    }
                },
                {
                    "name": "Факт (только Директ)",
                    "data": {
                        "19.01.2018": 432,
                        "18.01.2018": 434,
                        "17.01.2018": 516
                    }
                }
            ]
        }
    ]), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def front(path):
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return "Page not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8899, debug=True)
