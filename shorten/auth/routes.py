from . import auth

@auth.route('/')
def index():
    return 'Auth blueprint'

