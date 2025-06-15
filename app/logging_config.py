# app/logging_config.py

import logging.config
import yaml
import os

def setup_logging(default_path='app/logging.yaml', default_level=logging.INFO):
    if os.path.exists(default_path):
        with open(default_path, 'r') as f:
            config = yaml.safe_load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

def get_logger(name=None):
    import logging
    return logging.getLogger(name or "app")