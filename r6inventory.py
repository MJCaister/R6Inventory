from app import db
# form app.models import
from app import app


@app.shell_context_processor
def make_shell_context():
    return {'db': db}


if __name__ == '__main__':
    app.run(debug=True, port=8080, host='localhost')
