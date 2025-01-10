import json
from datetime import timedelta

from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS, cross_origin
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from Backend.BusinessLayer.NegevNerds import NegevNerds
from Backend.ServiceLayer.ServiceLayer import ServiceLayer

user_controller = Blueprint('user_controller', __name__)

CORS(user_controller, resources={
    r"/api/*": {
        "origins": "*",  # Or specify exact origin like "http://localhost:3000"
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})


serviceLayer = ServiceLayer(NegevNerds("../"))


def parse_jsonify(parsed_result):
    # Check the status and return appropriate response
    if parsed_result['status'] == 'success':
        return jsonify({
            "success": True,
            "message": parsed_result['message']
        }), 200
    else:
        return jsonify({
            "success": False,
            "message": parsed_result['message']
        }), 400


@user_controller.route('/api/register', methods=['POST', 'OPTIONS'])
@cross_origin()
def register():
    # Handle OPTIONS preflight request
    if request.method == 'OPTIONS':
        response = jsonify(success=True)
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

    try:
        # Extract data from the request
        data = request.get_json()

        # Validate input
        if not all(key in data for key in ['email', 'password','password_confirm', 'first_name', 'last_name']):
            return jsonify({
                "success": False,
                "message": "Missing required fields"
            }), 400

        # Extract data
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        password_confirm = data.get('password_confirm')

        # Call the service layer's register method directly
        result = serviceLayer.register(email, password,password_confirm, first_name, last_name)

        # Parse the JSON string
        # parsed_result = json.loads(result)

        # # return parse_jsonify(parsed_result)
    
        # if result['status'] == "success":
        #     return jsonify({
        #         "success": True,
        #         "message": parsed_result['message'],
        #         "password": parsed_result['password']  # Include password if needed
        #     }),200
        
        if result['status'] == "success":
            return jsonify({"success": True, "message": result["message"], "password": result["password"]}), 200
        return jsonify({"success": False, "message": result["message"]}), 400

    except json.JSONDecodeError:
        # Handle JSON decoding error
        return jsonify({
            "success": False,
            "message": "Invalid JSON response from service"
        }), 500
    except Exception as e:
        print(f"Error in registration: {str(e)}")
        return jsonify({
            "success": False,
            "message": "An unexpected error occurred",
            "error": str(e)
        }), 500


@user_controller.route('/api/register_authentication_part', methods=['POST', 'OPTIONS'])
@cross_origin()
def register_authentication_part():
    # Handle OPTIONS preflight request
    if request.method == 'OPTIONS':
        response = jsonify(success=True)
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

    try:
        # Extract data from the request
        data = request.get_json()

        # Validate input
        if not all(key in data for key in ['auth_code', 'email']):
            return jsonify({
                "success": False,
                "message": "Missing required fields"
            }), 400

        # Extract data
        auth_code = data.get('auth_code')

        email = data.get('email')

        # Call the service layer's register method directly
        result = serviceLayer.register_authentication_part(email, auth_code)

        # Parse the JSON string
        parsed_result = json.loads(result)

        # Check the status and return appropriate response
        if parsed_result['status'] == 'success':
            return jsonify({
                "success": True,
                "message": parsed_result['message']
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": parsed_result['message']
            }), 400

    except json.JSONDecodeError:
        # Handle JSON decoding error
        return jsonify({
            "success": False,
            "message": "Invalid JSON response from service"
        }), 500
    except Exception as e:
        print(f"Error in registration: {str(e)}")
        return jsonify({
            "success": False,
            "message": "An unexpected error occurred",
            "error": str(e)
        }), 500


@user_controller.route('/api/register_termOfUse_part', methods=['POST', 'OPTIONS'])
@cross_origin()
def register_termOfUse_part():
    # Handle OPTIONS preflight request
    if request.method == 'OPTIONS':
        response = jsonify(success=True)
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

    try:
        # Extract data from the request
        data = request.get_json()

        # Validate input
        if not all(key in data for key in ['email', 'password', 'first_name', 'last_name']):
            return jsonify({
                "success": False,
                "message": "Missing required fields"
            }), 400

        # Extract data
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')

        # Call the service layer's register method directly
        result = serviceLayer.register_termOfUse_part(email, password, first_name, last_name)

        # Parse the JSON string
        parsed_result = json.loads(result)

        # Check the status and return appropriate response
        if parsed_result['status'] == 'success':
            user_id = parsed_result.get('user_id')  # assuming user_id is returned from your service layer
            access_token = create_access_token(identity=user_id, expires_delta=timedelta(hours=10))
            print("token: ", access_token)
            return jsonify({
                "success": True,
                "message": parsed_result['message'],
                "user_id": parsed_result['user_id'],  # Explicitly fetch user_id
                "access_token": access_token,  # Include the generated token in the response
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": parsed_result['message']
            }), 400

    except json.JSONDecodeError:
        # Handle JSON decoding error
        return jsonify({
            "success": False,
            "message": "Invalid JSON response from service"
        }), 500
    except Exception as e:
        print(f"Error in registration: {str(e)}")
        return jsonify({
            "success": False,
            "message": "An unexpected error occurred",
            "error": str(e)
        }), 500

# @user_controller.route('/api/login', methods=['POST', 'OPTIONS'])
# @cross_origin()
# def login_user():
#     # Handle OPTIONS preflight request
#     if request.method == 'OPTIONS':
#         response = jsonify(success=True)
#         response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
#         response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
#         response.headers.add('Access-Control-Allow-Methods', 'POST')
#         return response

#     try:
#         # Extract data from the request
#         data = request.get_json()

#         # Validate input
#         if not all(key in data for key in ['email', 'password']):
#             return jsonify({
#                 "success": False,
#                 "message": "Missing required fields"
#             }), 400

#         # Extract data
#         email = data.get('email')
#         password = data.get('password')

#         # Call the service layer's login method directly
#         result = serviceLayer.login(email, password)

#         # Parse the JSON string
#         parsed_result = json.loads(result)

#         # Check the status and return appropriate response
#         if parsed_result['status'] == 'success':
#             return jsonify({
#                 "success": True,
#                 "message": parsed_result['message'],
#                 "user_id": parsed_result['user_id'] , # Explicitly fetch user_id
#                 "first_name": parsed_result['first_name'],
#                 "last_name": parsed_result['last_name'],
#             }), 200
#         else:
#             return jsonify({
#                 "success": False,
#                 "message": parsed_result['message']
#             }), 400

#     except json.JSONDecodeError:
#         # Handle JSON decoding error
#         return jsonify({
#             "success": False,
#             "message": "Invalid JSON response from service"
#         }), 500
#     except Exception as e:
#         print(f"Error in login: {str(e)}")
#         return jsonify({
#             "success": False,
#             "message": "An unexpected error occurred",
#             "error": str(e)
#         }), 500
# @user_controller.route('/api/login', methods=['POST', 'OPTIONS'])
# @cross_origin()
# def login_user():
#     # Handle OPTIONS preflight request
#     if request.method == 'OPTIONS':
#         response = jsonify(success=True)
#         response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
#         response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
#         response.headers.add('Access-Control-Allow-Methods', 'POST')
#         return response

#     try:
#         # Extract data from the request
#         data = request.get_json()

#         # Validate input
#         if not data or not all(key in data for key in ['email', 'password']):
#             print("Login failed: Missing required fields")
#             return jsonify({
#                 "success": False,
#                 "message": "Missing required fields"
#             }), 400

#         # Extract email and password
#         email = data.get('email')
#         password = data.get('password')

#         # Log the login attempt
#         print(f"Login attempt: email={email}")

#         # Call the service layer's login method
#         result = serviceLayer.login(email, password)

#         # Parse the JSON string
#         parsed_result = json.loads(result)

#         # Check the status and return appropriate response
#         if parsed_result.get('status') == 'success':
#             print(f"Login successful for user: {email}")
#             return jsonify({
#                 "success": True,
#                 "message": parsed_result.get('message'),
#                 "user_id": parsed_result.get('user_id'),
#                 "first_name": parsed_result.get('first_name'),
#                 "last_name": parsed_result.get('last_name'),
#             }), 200
#         else:
#             print(f"Login failed for user: {email} - Reason: {parsed_result.get('message')}")
#             return jsonify({
#                 "success": False,
#                 "message": parsed_result.get('message', 'Login failed')
#             }), 400

#     except json.JSONDecodeError as e:
#         print(f"JSON Decode Error in login: {str(e)}")
#         return jsonify({
#             "success": False,
#             "message": "Invalid JSON response from service"
#         }), 500
#     except Exception as e:
#         print(f"Unexpected error in login: {str(e)}")
#         return jsonify({
#             "success": False,
#             "message": "An unexpected error occurred",
#             "error": str(e)
#         }), 500


@user_controller.route('/api/login', methods=['POST', 'OPTIONS'])
@cross_origin()
def login_user():
    if request.method == 'OPTIONS':
        response = jsonify(success=True)
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

    try:
        data = request.get_json()

        # Validate input
        if not all(key in data for key in ['email', 'password']):
            return jsonify({
                "success": False,
                "message": "Missing required fields"
            }), 400

        email = data.get('email')
        password = data.get('password')

        # Call service layer
        result = serviceLayer.login(email, password)

        parsed_result = json.loads(result)

        # Validate parsed_result structure
        if not parsed_result or parsed_result.get('status') != 'success':
            return jsonify({
                "success": False,
                "message": parsed_result.get('message', 'Login failed')
            }), 400

        user_id = parsed_result.get('user_id')  # assuming user_id is returned from your service layer
        access_token = create_access_token(identity=user_id, expires_delta=timedelta(hours=10))
        print("token: ", access_token)

        # Successful login response
        return jsonify({
            "success": True,
            "message": parsed_result.get('message'),
            "user_id": parsed_result.get('user_id'),
            "first_name": parsed_result.get('first_name'),
            "last_name": parsed_result.get('last_name'),
            "access_token": access_token,
        }), 200

    except Exception as e:
        print(f"Error in login: {str(e)}")
        return jsonify({
            "success": False,
            "message": "An unexpected error occurred",
            "error": str(e)
        }), 500


@user_controller.route('/api/logout', methods=['POST', 'OPTIONS'])
@cross_origin()
@jwt_required()
def logout_user():
    # Handle OPTIONS preflight request
    if request.method == 'OPTIONS':
        response = jsonify(success=True)
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

    try:
        # Get user identity from the JWT token
        current_user = get_jwt_identity()  # שמור את המידע מתוך ה-JWT
        print(f"Current user from JWT: {current_user}")  # הדפסת המידע שנמצא בטוקן

        # Call the service layer's logout method directly
        result = serviceLayer.logout(current_user)
        print(f"Logout result from service layer: {result}")  # הדפסת תוצאת פעולת ה-logout

        # Parse the JSON string
        parsed_result = json.loads(result)
        print(f"Parsed result: {parsed_result}")  # הדפסת התוצאה אחרי הפענוח

        return parse_jsonify(parsed_result)

    except json.JSONDecodeError:
        # Handle JSON decoding error
        print("Error decoding JSON")  # הדפסת הודעה אם יש בעיה בפענוח ה-JSON
        return jsonify({
            "success": False,
            "message": "Invalid JSON response from service"
        }), 500
    except Exception as e:
        print(f"Error in logout: {str(e)}")  # הדפסת שגיאה במקרה של בעיה אחרת
        return jsonify({
            "success": False,
            "message": "An unexpected error occurred",
            "error": str(e)
        }), 500


@user_controller.route('/api/get_user_courses', methods=['GET', 'OPTIONS'])
@cross_origin()
@jwt_required()
def get_user_courses():
    # Handle OPTIONS preflight request
    if request.method == 'OPTIONS':
        response = jsonify(success=True)
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET')
        return response

    try:
        current_user = get_jwt_identity()

        # Fetch the user courses from the service layer
        result = serviceLayer.get_user_courses(current_user)  # השתמש במידע מתוך הטוקן

        result = json.loads(result)  # Convert the JSON string to a Python dict

        if 'data' in result:
            parsed_result = result["data"]  # Now we're getting only the courses list

        # Return the courses as JSON response
        return jsonify({
            "success": True,
            "courses": parsed_result
        }), 200

    except Exception as e:
        print(f"Error in getting user courses: {str(e)}")
        return jsonify({
            "success": False,
            "message": "An unexpected error occurred",
            "error": str(e)
        }), 500

    except json.JSONDecodeError:
        # Handle JSON decoding error
        return jsonify({
            "success": False,
            "message": "Invalid JSON response from service"
        }), 500
    except Exception as e:
        print(f"Error in get user courses: {str(e)}")
        return jsonify({
            "success": False,
            "message": "An unexpected error occurred",
            "error": str(e)
        }), 500


@user_controller.route('/api/get_user_name', methods=['GET', 'OPTIONS'])
@cross_origin()
@jwt_required()
def get_user_name():
    # Handle OPTIONS preflight request
    if request.method == 'OPTIONS':
        response = jsonify(success=True)
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET')
        return response

    try:
        user_id = request.args.get('user_id')  # Get the user_id from query parameters

        # Fetch the user courses from the service layer
        result = serviceLayer.get_user_name(user_id)

        result = json.loads(result)  # Convert the JSON string to a Python dict

        if 'data' in result:
            parsed_result = result["data"]  # Now we're getting only the courses list

        # Return the courses as JSON response
        return jsonify({
            "success": True,
            "data": parsed_result
        }), 200

    except Exception as e:
        print(f"Error in getting user name: {str(e)}")
        return jsonify({
            "success": False,
            "message": "An unexpected error occurred",
            "error": str(e)
        }), 500

    except json.JSONDecodeError:
        # Handle JSON decoding error
        return jsonify({
            "success": False,
            "message": "Invalid JSON response from service"
        }), 500