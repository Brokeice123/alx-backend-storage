#!/usr/bin/env python3
""" 
Script that lists all documents in a collection
 """


def list_all(mongo_collection):
    """ returns all documents in a collection """
    doc = mongo_collection.find()
    return [a for a in doc]
