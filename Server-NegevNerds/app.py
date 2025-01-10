import datetime

from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

from waitress import serve
from multiprocessing import cpu_count

from Backend.API_Communication.UserController import user_controller
from Backend.API_Communication.CourseController import course_controller
from Backend.BusinessLayer.NegevNerds import NegevNerds
from Backend.ServiceLayer.ServiceLayer import ServiceLayer

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'negev_nerds'  # סוד ה-JWT שלך
jwt = JWTManager(app)

db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///NegevNerds.db'  # For SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
migrate = Migrate(app, db)

CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://132.72.116.86:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})


# Register controllers
app.register_blueprint(user_controller)
app.register_blueprint(course_controller)


@app.route('/api/<path:path>', methods=['OPTIONS'])
def handle_options(path):
    response = app.make_response('')
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PUT, DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


@app.errorhandler(401)
def custom_401(error):
    return jsonify({
        "success": False,
        "message": "Unauthorized access, please provide a valid token"
    }), 401


def main():
    #
    # db.init_app(app)
    #
    # with app.app_context():
    #     db.create_all()

    print("Starting the Exam Preparation System API...")


    service_layer = ServiceLayer(NegevNerds("../"))
    service_layer.initialize_system()

    threads = (cpu_count() * 2) + 1
    serve(app, host='0.0.0.0', port=5001, threads=threads)

    #app.run(debug=True, host='0.0.0.0', port=5001, use_reloader=False , threaded=True)


if __name__ == "__main__":
    main()


