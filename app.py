from flask import Flask
from routes.extract_routes import extract_bp
from routes.history_routes import history_bp
from routes.auth_routes import auth_bp

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

app.register_blueprint(extract_bp)
app.register_blueprint(history_bp)
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=True)
