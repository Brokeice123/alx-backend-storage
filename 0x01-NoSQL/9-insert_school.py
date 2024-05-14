#!/usr/bin/env python3
"""
Script that inserts a new document
based on kwargs in a collection
"""

def insert_school(mongo_collection, **kwargs):
    """Insert a new document in a collection based on kwargs"""
    return mongo_collection.insert_one(kwargs).inserted_id
