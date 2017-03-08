#!/usr/bin/env python3

docstring = """This is the main api which will be started by running run.sh"""

import hug
import falcon
from logger import log
import logging
from db import KaranaDBWrapper
from jwtoken import JWTWrapper
import json#


module_log = logging.getLogger(__name__)
log.info(docstring)
module_log.info('test for logger name __name__')

db = KaranaDBWrapper()
jwtoken = JWTWrapper(db)
token_key_authentication = hug.authentication.token(jwtoken.token_verify)

origin = 'http://localhost:3000'

@hug.request_middleware()
def process_cors(request, response):
    log.info('This is how the request looks like:' + request.method)
    response.set_header('Access-Control-Allow-Origin', origin)
    if request.get_header('Access-Control-Request-Method') == 'POST':
        response.set_header('Access-Control-Allow-Methods', 'POST')
    elif request.get_header('Access-Control-Request-Method') == 'PUT':
        response.set_header('Access-Control-Allow-Methods', 'PUT')
    response.set_header('Access-Control-Allow-Headers', 'content-type')


@hug.get('/{resources}/{resource_id}/', version=1, requires=token_key_authentication)
def get_resource(resources: hug.types.text, resource_id: hug.types.text, response):
    """This method returns either the resource with given ID or all resources"""
    if resources == 'v1': # This is necessary when resource_id is empty
        resources = resource_id
        resource_id = ''
    try:
        log.debug('Trying get Resource for resource: ' + resources + ' with id: ' + resource_id)
        if resource_id == '':
            all_res = db.get_res(resources)
            results = {'results': [all_res]}
            if results['results'][0] or results['results'][0] == {}:
                return json.dumps(results)
        else:
            results = {'results': [{resource_id: db.get_res_by_id(resources, resource_id)}]}
            if results['results'][0][resource_id]:
                return json.dumps(results)
        log.error('Results: ' + str(results))
        raise
    except Exception as e:
        log.error('Couldnt get Resource for resource: ' + resources + ' with id: ' + resource_id)
        raise falcon.HTTPBadRequest('Get Resource Error', 'Failed to get requested resources Resource')


@hug.post('/{resources}/new/', version=1,requires=token_key_authentication)
def create_resource(resources: hug.types.text, data, response):
    """This method creates a resource"""
    log.debug("Incoming data is_ " + str(data))
    if resources == 'v1':  # This is necessary when resource_id is empty
        return False
    try:
        results = {'results': [{'uuid': db.add_new_res(resources, str(data))}]}
        if results['results'][0]['uuid']:
            return json.dumps(results)
        raise
    except Exception as e:
        log.error('Could not Create Resource: ' + resources + ' with data: ' + str(data))
        raise falcon.HTTPBadRequest('Create Resource Error', 'Failed to create new Resource')


@hug.post('/{resources}/login/', version=1)
def login_resource(resources: hug.types.text, user, password, response):
    """This method creates a resource"""
    log.debug("Incoming data is_ " + str(user))
    if resources == 'v1':  # This is necessary when resource_id is empty
        return False
    try:
        results = {'results': [{'token': jwtoken.token_generate(user, password, resources)}]}
        if results['results'][0]['token']:
            return json.dumps(results)
        raise
    except Exception as e:
        log.error('Could not login Resource: ' + resources + ' with username: ' + str(user),e)
        raise falcon.HTTPBadRequest('Create Resource Error', 'Could not login Resource')


@hug.put('/{resources}/{resource_id}/', version=1,requires=token_key_authentication)
def updated_resource(resources: hug.types.text, resource_id: hug.types.text, data, response):
    """This method updates a resource completely"""
    if resources == 'v1':  # This is necessary when resource_id is empty
        return False
    try:
        results = {'results': [{resource_id: db.update_res(resources, resource_id, str(data))}]}
        log.debug('Results ' + str(results))

        if results['results'][0][resource_id]:
            return json.dumps(results)
        raise
    except Exception as e:
        log.error('Could not update Resource: ' + resources + ' with data: ' + str(data),e)
        raise falcon.HTTPBadRequest('Update Resource Error', 'Failed to update Resource')


@hug.patch('/{resources}/{resource_id}/', version=1,requires=token_key_authentication)
def modify_resource(resources: hug.types.text, resource_id: hug.types.text, data, response):
    """"This method modifies a resource in this case only one field allowed"""
    if resources == 'v1':  # This is necessary when resource_id is empty
        return False
    try:
        results = {'results': [{resource_id: db.modify_res(resources, resource_id, str(data))}]}
        log.debug('Results ' + str(results))
        if results['results'][0][resource_id]:
            return json.dumps(results)
        raise
    except Exception as e:
        log.error('Could not modify Resource: ' + resources + ' with data: ' + str(data))
        raise falcon.HTTPBadRequest('Modify Resource Error', 'Failed to modify Resource')


@hug.delete('/{resources}/{resource_id}/', version=1,requires=token_key_authentication)
def delete_resource(resources: hug.types.text, resource_id: hug.types.text, response):
    """This method deletes a resource"""
    if resources == 'v1':  # This is necessary when resource_id is empty
        return False
    try:
        resp = db.get_res_by_id(resources, resource_id)
        if resp:
            all_res = db.rm_res(resources, resource_id)
            results = {'results': [all_res]}
            if results['results'][0] or results['results'][0] == {}:
                return json.dumps(results)
        log.error('Results: ' + str(results))
        raise
    except Exception as e:
        log.error('Could not delete Resource: ' + resources + ' with uuid ' + resource_id)
        raise falcon.HTTPBadRequest('Delete Resource Error', 'Failed to delete Resource')

@hug.post('/sync/db/all', version=1,requires=token_key_authentication)
def sync_db_all_states(response):
    try:
        if not db.__sync_state_action__() or db.__update_uniqueness_index__():
            raise
    except Exception as e:
        log.error('Failed Synching Database')
        raise falcon.HTTPBadRequest('Sync DB error', 'Failed to sync db')
