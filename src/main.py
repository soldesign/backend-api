#!/usr/bin/env python3

docstring = """This is the main api which will be started by running run.sh"""

import hug
from log import log

log.info(docstring)


@hug.get('{resources}/{resources_id}', version=1)
def get_resource():
    """This method returns either the resource with given ID or al resources"""


@hug.post('{resources}/new', version=1)
def create_resource():
    """This method creates a resource"""


@hug.put('{resources}/{resource_id}', version=1)
def updated_resource():
    """This method updates a resource completely"""


@hug.patch('{resources}/{resource_id}', version=1)
def modify_resource():
    """"This method modifies a resource in this case only one field allowed"""


@hug.delete('{resources}/{resource_id}', version=1)
def delete_resource():
    """This method deletes a resource"""

