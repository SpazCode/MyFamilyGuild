#!/usr/bin/env python3
import json


def load_json(filepath):
    res = {}
    with open(filepath) as f:
        res = json.load(f)
    return res


def check_type(obj, target_class):
    if type(obj).__name__ == target_class:
        return True
    for classes in type(obj).__bases__:
        if classes.__name__ == target_class:
            return True
    raise InvalidTypeExceptipn(
        str(obj) + " is not of the class named " + str(target_class))


class InvalidTypeExceptipn(Exception):
    pass
