#!/usr/bin/env python3

docstring = """This is the main api which will be started by running run.sh"""

import hug
from log import log
import logging
module_log = logging.getLogger(__name__)
log.info(docstring)
module_log.info('test for logger name __name__')

@hug.get('/{resources}/{resource_id}/', version=1)
def get_resource(resources: hug.types.text, resource_id: hug.types.text):
    """This method returns either the resource with given ID or al resources"""
    return True


@hug.post('/{resources}/new/', version=1)
def create_resource(resources: hug.types.text, body):
    """This method creates a resource"""
    return True


@hug.put('/{resources}/{resource_id}/', version=1)
def updated_resource(resources: hug.types.text, resource_id: hug.types.text, body):
    """This method updates a resource completely"""
    return True


@hug.patch('/{resources}/{resource_id}/', version=1)
def modify_resource(resources: hug.types.text, resource_id: hug.types.text, body):
    """"This method modifies a resource in this case only one field allowed"""
    return True


@hug.delete('/{resources}/{resource_id}/', version=1)
def delete_resource(resources: hug.types.text, resource_id: hug.types.text):
    """This method deletes a resource"""
    return True

