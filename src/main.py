#!/usr/bin/env python3

docstring = """This is the main api which will be started by running run.sh"""

import hug
from log import log
import logging
from db import KaranaDBWrapper
module_log = logging.getLogger(__name__)
log.info(docstring)
module_log.info('test for logger name __name__')

db = KaranaDBWrapper()

@hug.get('/{resources}/{resource_id}/', version=1)
def get_resource(resources: hug.types.text, resource_id: hug.types.text):
    """This method returns either the resource with given ID or all resources"""
    if resources == 'v1': # This is necessary when resource_id is empty
        resources = resource_id
        resource_id = ''
    try:

        return str(db.get_db_dump())
    except Exception:
        log.error('Couldnt get Resource for resource: ' + resources + ' with id: ' + resource_id)
        return False


@hug.post('/{resources}/new/', version=1)
def create_resource(resources: hug.types.text, body):
    """This method creates a resource"""
    if resources == 'v1':  # This is necessary when resource_id is empty
        return False
    try:
        return db.add_new_res(resources, body)
    except Exception:
        log.error('Couldnot Create Resource: ' + resources + ' with body: ' + body)
        return False


@hug.put('/{resources}/{resource_id}/', version=1)
def updated_resource(resources: hug.types.text, resource_id: hug.types.text, body):
    """This method updates a resource completely"""
    if resources == 'v1':  # This is necessary when resource_id is empty
        return False
    try:
        return True
    except Exception:
        log.error('Couldnot Update Resource: ' + resources + ' resource_id: ' + resource_id + ' body: ' + body)
        return False


@hug.patch('/{resources}/{resource_id}/', version=1)
def modify_resource(resources: hug.types.text, resource_id: hug.types.text, body):
    """"This method modifies a resource in this case only one field allowed"""
    if resources == 'v1':  # This is necessary when resource_id is empty
        return False
    try:
        return True
    except Exception:
        log.error('Couldnot Modify Resource: ' + resources + ' resource_id: ' + resource_id + ' body: ' + body)
        return False


@hug.delete('/{resources}/{resource_id}/', version=1)
def delete_resource(resources: hug.types.text, resource_id: hug.types.text):
    """This method deletes a resource"""
    if resources == 'v1':  # This is necessary when resource_id is empty
        return False
    try:
        #KaranaDBWrapper.rm_res()
        return True
    except Exception:
        log.error('Couldnot Update Resource: ' + resources + ' resource_id: ' + resource_id + ' body: ' + body)
        return False

