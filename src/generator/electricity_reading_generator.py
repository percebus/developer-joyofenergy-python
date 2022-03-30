from service.time_converter import iso_format_to_unix_time

import math
import random
import datetime


def random_int_between(min_val, max_val):
    return "%02d" % random.randrange(min_val, max_val)


def get_timedelta(sec=60):
    return datetime.timedelta(seconds=sec)


def get_datetime_ago(minutes):
    _datetime = datetime.datetime.now() - get_timedelta(minutes*60)
    return iso_format_to_unix_time(_datetime.isoformat())


def generate_random_reading():
    return math.floor(random.random() * 1000) / 1000


def generate_electricity_readings(num):
    return [
        {
            "time": get_datetime_ago(minutes=i),
            "reading": generate_random_reading()
        }
        for i in range(num)
    ]
