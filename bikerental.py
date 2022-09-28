from app import bikerental, db
from app.models import Users

@bikerental.shell_context_processor
def make_shell_context():
    return {'db': db, 'Users': Users}