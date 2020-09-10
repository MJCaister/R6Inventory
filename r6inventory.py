import sys

# form app.models import
# imports the flask app and database
from app import app
from app import db

print("\nPython Ver: " + sys.version + "\n")

# Makes the database callable in shell
@app.shell_context_processor
def make_shell_context():
    return {'db': db}

# Runs the application
# Debug should be turned off for live builds
if __name__ == '__main__':
    app.run(debug=True, port=8080, host='localhost')
