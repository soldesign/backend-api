#!/usr/bin/env python3

docstring = """This is the main api which will be started by running run.sh"""

import hug
import falcon
from log import log
import logging
from db import KaranaDBWrapper
module_log = logging.getLogger(__name__)
log.info(docstring)
module_log.info('test for logger name __name__')

db = KaranaDBWrapper()

@hug.get('/{resources}/{resource_id}/', version=1)
def get_resource(resources: hug.types.text, resource_id: hug.types.text, response):
    """This method returns either the resource with given ID or all resources"""
    if resources == 'v1': # This is necessary when resource_id is empty
        resources = resource_id
        resource_id = ''
    try:
        resp = db.get_db_dump()
        if resp:
            return str(resp)
        raise
    except:
        log.error('Couldnt get Resource for resource: ' + resources + ' with id: ' + resource_id)
        raise falcon.HTTPBadRequest('Get Resource Error', 'Failed to get requested resources Resource')


@hug.post('/{resources}/new/', version=1)
def create_resource(resources: hug.types.text, data):
    """This method creates a resource"""
    log.debug("Incoming data is_ " + str(data))
    if resources == 'v1':  # This is necessary when resource_id is empty
        return False
    try:
        resp = db.add_new_res(resources, str(data))
        if resp:
            return str(resp)
        raise
    except:
        log.error('Could not Create Resource: ' + resources + ' with data: ' + str(data))
        raise falcon.HTTPBadRequest('Create Resource Error', 'Failed to create new Resource')


@hug.put('/{resources}/{resource_id}/', version=1)
def updated_resource(resources: hug.types.text, resource_id: hug.types.text, data):
    """This method updates a resource completely"""
    if resources == 'v1':  # This is necessary when resource_id is empty
        return False
    try:
        resp = 0
        if resp:
            return str(resp)
        raise
    except:
        log.error('Could not update Resource: ' + resources + ' with data: ' + str(data))
        raise falcon.HTTPBadRequest('Update Resource Error', 'Failed to update Resource')


@hug.patch('/{resources}/{resource_id}/', version=1)
def modify_resource(resources: hug.types.text, resource_id: hug.types.text, data):
    """"This method modifies a resource in this case only one field allowed"""
    if resources == 'v1':  # This is necessary when resource_id is empty
        return False
    try:
        resp = 0
        if resp:
            return str(resp)
        raise
    except:
        log.error('Could not modify Resource: ' + resources + ' with data: ' + str(data))
        raise falcon.HTTPBadRequest('Modify Resource Error', 'Failed to modify Resource')


@hug.delete('/{resources}/{resource_id}/', version=1)
def delete_resource(resources: hug.types.text, resource_id: hug.types.text):
    """This method deletes a resource"""
    if resources == 'v1':  # This is necessary when resource_id is empty
        return False
    try:
        resp = 0
        if resp:
            return str(resp)
        raise
    except:
        log.error('Could not delete Resource: ' + resources)
        raise falcon.HTTPBadRequest('Delete Resource Error', 'Failed to delete Resource')

