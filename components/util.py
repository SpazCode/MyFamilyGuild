#!/usr/bin/env python3
import json


def load_json(filepath):
    res = {}
    with open(filepath) as f:
        res = json.load(f)
    return res
