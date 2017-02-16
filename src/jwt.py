#!/usr/bin/env python3

docstring=''' A basic example of authentication requests within a hug API, mostly copied from the hug example'''

import hug
import jwt
import logging
import crypt
import time
import random
import base64
from log import log
from db import KaranaDBWrapper
from configuration import loginresource

FORMAT = 'jwt-example log %(levelname)s: %(message)s'
logging.basicConfig(level=0, format=FORMAT)
logging.info(docstring)



########################################################################################################################
## this sections represents the example data for this run
########################################################################################################################

# this key should be generated from a function before the start of hug
applicationTokenKey = "GlobalKeyGeneratedOnEveryRun"
# for quicker chacking if token exists, otherwise redirect to token generation
globaltokenstate = {}

# userdata
## user-00001
plaintext_pwd_1 = 'total_beklopptes_pw'
# only this hashed password should be saved in the db
hashed_pwd_1 = hash_the_pw(plaintext_pwd_1)
user_00001 = {'login': {'name': 'micha@zufrieden.de',\
                        'pwhash': hashed_pwd_1},\
              'metadata': {'place': 'Berlin'}}

## user-00002
plaintext_pwd_2 = 'noch_ein_total_beklopptes_pw'
# only this hashed password should be saved in the db
hashed_pwd_2 = hash_the_pw(plaintext_pwd_2)
user_00002 = {'login': {'name': 'frank@zufrieden.de',\
                        'pwhash': hashed_pwd_2},\
              'metadata': {'place': 'Weißensee'}}

userdict = {'user-00001': user_00001, 'user-00002': user_00002}



loginnames = {}
for userid in userdict.keys():
    entry = userdict[userid]['login']
    logging.debug('entry in userdict:' + str(entry))
    try:
        loginname = entry['name']
        loginnames[loginname] = {'userid': userid, 'pwhash': entry['pwhash']}
    except:
        logging.warning("The following entry of the userdict is malformed: " + str(entry))

logging.warning('loginnames: ' + str(loginnames))

########################################################################################################################


class JWT_Wrapper():
    """JWT Wrapper class"""

    def __init__(self, db,  apikey = None, apikeygensize = 2048):
        log.debug("create the internal reference to the KaranaDBWrapper")
        if isinstance(db, KaranaDBWrapper):
            self.__db__ = db
        else:
            raise ValueError("The object behind the the given db reference is not an instance of KaranaDBWrapper, but of {0}".format(str(type(db))))

        if apikey == None:
            log.debug("askting the god of randomness for '" + \
                      str(apikeygensize) + \
                      "' random manabits to create the initialization api key. ")
            self.__apikey__ = base64.b64encode(random.getrandbits(apikeygensize).to_bytes(int(apikeygensize/8), "big"))[:-2]
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

    def __check_pwd__(self, username, input_pw):
        self.__db__["tables"][loginresource]###################################
        pass

    ## token_key verify
    def token_verify(self, token: hug.types.text):
        logging.info('try to verify this token: ' + str(token))
        for word in token.split(' '):
            try:
                validPayloadFromToken = jwt.decode(jwt=word, key=applicationTokenKey, verify=True, algorithms='HS256')
                logging.info('validPayloadFromToken: ' + str(validPayloadFromToken))
                return validPayloadFromToken
            except:
                logging.debug(
                    "This word in 'Authorization' field of the HTTP-Header is not a valid JWT token: '" + word + "'")
        return False


    def token_generate(self, username: hug.types.text, password: hug.types.text, usertable, tokenpayload=None):
        """Authenticate and return a token"""

        if tokenpayload == None:
            tokenpayload = self.__generate_login_payload__(username)

        saved_pw_hash =
        hashed_input_pw = self.__generate_pw_hash__(password, salt=usertable[username]['pwhash'][:19])

        logging.debug('loginnames: ' + str(loginnames))
        logging.debug('userdict: ' + str(userdict))
        logging.debug('submitted_username: ' + str(username))
        logging.debug('hash of submitted pw: ' + str(hashed_input_pw))

        # try:
        if username in loginnames.keys() and hashed_input_pw == loginnames[username]['pwhash']:
            userid = loginnames[str(username)]['userid']
            logging.debug('uderid: ' + str(userid))
            generated_token = jwt.encode(payload={'loginname': str(username), \
                                                  'data': userdict[userid]['metadata']}, \
                                         key=applicationTokenKey, \
                                         algorithm='HS256')
            add_token_to_tokenstate(generated_token)
            return {"token": generated_token}
        return 'Invalid username and/or password for user: {0}'.format(username)





jwthandler = JWT_Wrapper()


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



