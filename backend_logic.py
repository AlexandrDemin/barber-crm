#! /home/devel/anaconda2/envs/py35/bin/python3.6
# -*- coding: utf-8 -*-

import io
import pandas as pd
import numpy as np
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timedelta
import psycopg2
import requests
import time
import json
import math
import copy
import urllib.parse
import codecs
import random

# Получить проекты
def getData():
    return {
            "message": "Дратути"
        }
