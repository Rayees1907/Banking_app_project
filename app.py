from flask import Flask
from .routes import init_app_routes
from .models import init_db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_super_secret_key_here' # Change this in production!

# Initialize database
with app.app_context():
    init_db()

# Initialize routes
init_app_routes(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')