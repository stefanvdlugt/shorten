import os
from dotenv import load_dotenv
from uuid import uuid4

basedir = os.environ.get('BASEDIR',os.path.abspath(os.path.dirname(__file__)))
load_dotenv(dotenv_path=os.path.join(basedir,'settings.env'))

def get_secret_key():
    # Try reading secret key from environment
    key = os.environ.get('SECRET_KEY')
    if not key:
        # If a secret key is not defined in the environment, try reading one
        # from a file, and otherwise, generate a key and store it in a file. 
        keyfile = os.path.join(basedir,'secret_key')
        if os.path.isfile(keyfile):
            with open(keyfile,'r') as f:
                key = f.read().rstrip('\n')
        else:
            key = str(uuid4())
            um = os.umask(0o077) # don't give other users read access
            with open(keyfile,'w') as f:
                f.write(key)
            os.umask(um) # revert umask to original
    return key

class Config(object):
    SERVER_NAME = os.environ.get('SERVER_NAME') or 'localhost:5000'
    BASE_URL = os.environ.get('BASE_URL') or ''

    SECRET_KEY = get_secret_key()

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.environ.get(
        'DATABASE_PATH', os.path.join(basedir, 'app.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
