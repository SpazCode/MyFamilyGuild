#!/usr/bin/env python3
import json
import inspect


def load_json(filepath):
    res = {}
    with open(filepath) as f:
        res = json.load(f)
    return res


def check_type(obj, target_class):
    for classes in inspect.getmro(type(obj)):
        if classes.__name__ == target_class:
            return True
    raise InvalidTypeExceptipn(
        str(obj) + " is not of the class named " + str(target_class))


class InvalidTypeExceptipn(Exception):
    pass
