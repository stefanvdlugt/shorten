from shorten import create_app, db
from shorten.models import User, ShortenedURL

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'ShortenedURL': ShortenedURL
    }
