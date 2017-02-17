import logging
import logging.config
import yaml
import os
configPath = 'logging.yaml.sample' #path has to be relative to script calling main.py
defaultLevel = logging.DEBUG
if os.path.exists(configPath):
    with open(configPath, 'rt') as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
else:
    logging.basicConfig(level=defaultLevel)
    logging.error('Could not find logging config file')


log = logging.getLogger('karana_backend_api')
