# coding: utf8

import hashlib


def sha1(bs):
    return hashlib.sha1(bs).hexdigest()
