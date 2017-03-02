#!/usr/bin/env python3

docstring = ''' The JWT-Wrapper implementation which makes it possible to sign data on the api backend. '''

import hug
import jwt
import crypt
import time
import random
import base64
from logger import log
from db import KaranaDBWrapper
from configuration import api_metadata
from configuration import resources


class JWTWrapper():
    """JWT Wrapper class"""

    def __init__(self, db, apikey=None, apikeygensize=2048):
        log.debug("create the internal reference to the KaranaDBWrapper")
        if isinstance(db, KaranaDBWrapper):
            self.__db__ = db
        else:
            raise ValueError(
                "The object behind the the given db reference is not an instance of KaranaDBWrapper, but of {0}".format(
                    str(type(db))))

        if apikey == None:
            log.debug("asking the god of randomness for '" + \
                      str(apikeygensize) + \
                      "' random manabits to create the initialization api key. ")
            self.__apikey__ = base64.b64encode(
                random.getrandbits(apikeygensize).to_bytes(int(apikeygensize / 8), "big"))[:-2]
        else:
            log.debug("\napikey variable was given at start time and is not generated. \
            This is only in a non productive or cluster setup with additional precautions ok. \
            Use it with care!\n")
            self.__apikey__ = str(apikey)

    def __generate_login_payload__(self, user):
        pass

    def __generate_pw_hash__(self, plaintext_pw, salt=crypt.mksalt(method=crypt.METHOD_SHA512)):
        assert isinstance(plaintext_pw, object)
        return crypt.crypt(plaintext_pw, salt=salt)

    def __check_credentials__(self, **kwargs):
        pass

    def __login_known__(self, remotelogin):
        loginresource = api_metadata['tenant_login_credentials_resource']
        # credentials
        # if remotelogin in db.uniqueness_index[]
        pass


        # for res in resources:
        #     if ("credentials_login_field" in res["metadata"].keys()) and (res["metadata"]["credentials_login_field"] not in  [None, "", " "])

        # else:
        #     logging.warning("No credentials_login_field defined. No login possible")
        #     return False

        # loginable_resources =
        # loginkeylist = db.tables[]
        # self.__db__["tables"]###################################
        # get the credentials from config and db

    ## token_key verify
    def token_verify(self, token: hug.types.text):
        log.info('try to verify this token: ' + str(token))
        for word in token.split(' '):
            try:
                validPayloadFromToken = jwt.decode(jwt=word, key=self.__apikey__, verify=True, algorithms='HS256')
                log.info('validPayloadFromToken: ' + str(validPayloadFromToken))
                return validPayloadFromToken
            except Exception as e:
                log.debug(
                    "This word in 'Authorization' field of the HTTP-Header is not a valid JWT token: '" + word + "'", e)
        return False

    def get_token(self, credentials):
        pass
        # if self.__check_credentials__(credentials) :

    def token_generate(self, resname: hug.types.text, password: hug.types.text, res, tokenpayload=None):
        """Authenticate and return a token"""

        if tokenpayload == None:
            tokenpayload = self.__generate_login_payload__(resname)

        login_field = self.__db__.main_state['table_meta']['resConfig'][res]['metadata']['credentials_login_field']
        log.debug('login field: ' + str(login_field))
        try:
            """This should fail if the user does not exist"""
            res_table = self.__db__.main_state['uniqueness_index'][res][login_field]
            log.debug('res: ' + str(res_table[resname]))
            hashed_input_pw = self.__generate_pw_hash__(password,
                                                        salt=res_table[resname]['credentials']['password'][:19])
            log.debug('hash of submitted pw: ' + str(hashed_input_pw))
        except:
            return False

        try:
            if hashed_input_pw == res_table[resname]['credentials']['password']:
                uuid = res_table[resname]['uuid']
                log.debug('uuid: ' + str(uuid))
                generated_token = jwt.encode(payload={'loginname': resname, \
                                                      'data': {'role': res_table[resname]['role']}}, \
                                             key=self.__apikey__, \
                                             algorithm='HS256')
                # add_token_to_tokenstate(generated_token)
                log.debug(str(generated_token))

                return generated_token.decode('utf-8')
            else:
                return False
        except:
            return False


# testdb = KaranaDBWrapper()
# jwthandler = JWT_Wrapper(testdb)

'''
token_key_authentication = hug.authentication.token(jwthandler.token_verify)
###


@hug.get('/token_authenticated', requires=token_key_authentication)
def token_auth_call(user: hug.directives.user):  # <- hug.directives.user?
    logging.info('vars in function namespace: ' + str(vars()))
    logging.info('user variable: ' + str(user))
    return 'You are authenticated'


@hug.post('/token_generation')
def token_gen_call(username: hug.types.text, password: hug.types.text):
    """Authenticate and return a token"""

    hashed_input_pw = hash_the_pw(password, salt=loginnames[username]['pwhash'][:19])

    logging.debug('loginnames: ' + str(loginnames))
    logging.debug('userdict: ' + str(userdict))
    logging.debug('submitted_username: ' + str(username))
    logging.debug('hash of submitted pw: ' + str(hashed_input_pw))

    #try:
    if username in loginnames.keys() and hashed_input_pw == loginnames[username]['pwhash']:
        userid = loginnames[str(username)]['userid']
        logging.debug('uderid: ' + str(userid))
        generated_token = jwt.encode(payload={'loginname': str(username), \
                                              'data': userdict[userid]['metadata']},\
                                     key=applicationTokenKey, \
                                     algorithm='HS256')
        add_token_to_tokenstate(generated_token)
        return {"token" : generated_token}
    return 'Invalid username and/or password for user: {0}'.format(username)
    #except:
    #    logging.warning("invalid token generation error!! bug in token generation?")
     #   return 'Invalid username and/or password.'
'''
